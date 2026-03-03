from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class WorkflowFeatures:
    jobs: int
    steps: int
    matrix_variants: int
    uses_cache_step: bool
    dependency_install_steps: int


@dataclass
class RunRecord:
    run_id: str
    workflow_name: str
    features: WorkflowFeatures
    predicted_minutes: float
    baseline_cost_usd: float

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["features"] = asdict(self.features)
        return payload


@dataclass
class OptimizationPlan:
    bottlenecks: list[str]
    cost_savings_estimate: float
    action_plan: list[str]
    optimized_minutes: float
    optimized_monthly_cost_usd: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
