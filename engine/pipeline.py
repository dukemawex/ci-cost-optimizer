from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any

from engine.memo import generate_memo_with_gemini
from engine.models import RunRecord
from engine.optimizer import build_recommendation_memo
from engine.predictor import estimate_monthly_cost, predict_runtime_minutes
from engine.sources import fetch_ci_sources
from engine.workflow_parser import parse_workflow


ARTIFACT_DIR = Path("artifacts")


def _write_json(filename: str, payload: Any) -> None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    (ARTIFACT_DIR / filename).write_text(json.dumps(payload, indent=2), encoding="utf-8")


def analyze_workflow(yaml_text: str, monthly_runs: int = 300) -> dict[str, Any]:
    workflow_name, features = parse_workflow(yaml_text)
    predicted_minutes = predict_runtime_minutes(features)
    monthly_cost = estimate_monthly_cost(predicted_minutes, monthly_runs)

    run_record = RunRecord(
        run_id=str(uuid.uuid4()),
        workflow_name=workflow_name,
        features=features,
        predicted_minutes=predicted_minutes,
        baseline_cost_usd=monthly_cost,
    )

    plan = build_recommendation_memo(features, predicted_minutes, monthly_cost, monthly_runs)
    default_memo = {
        "bottlenecks": plan.bottlenecks,
        "cost_savings_estimate": plan.cost_savings_estimate,
        "action_plan": plan.action_plan,
    }
    memo = generate_memo_with_gemini(default_memo)
    sources = fetch_ci_sources()

    _write_json("runs.json", [run_record.to_dict()])
    _write_json("predictions.json", {
        "predicted_runtime_minutes": predicted_minutes,
        "monthly_runs": monthly_runs,
        "estimated_monthly_cost_usd": monthly_cost,
    })
    _write_json("optimization_plan.json", {
        **plan.to_dict(),
        "gemini_memo": memo,
    })
    _write_json("sources.json", sources)

    return {
        "workflow_name": workflow_name,
        "predicted_runtime_minutes": predicted_minutes,
        "estimated_monthly_cost_usd": monthly_cost,
        "optimized_monthly_cost_usd": plan.optimized_monthly_cost_usd,
        "recommendations": memo,
        "sources": sources,
    }
