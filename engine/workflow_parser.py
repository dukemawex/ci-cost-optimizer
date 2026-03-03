from __future__ import annotations

from typing import Any

import yaml

from engine.models import WorkflowFeatures


class WorkflowParseError(ValueError):
    pass


def _matrix_variants(strategy_matrix: Any) -> int:
    if not isinstance(strategy_matrix, dict):
        return 1

    variants = 1
    for value in strategy_matrix.values():
        if isinstance(value, list) and value:
            variants *= len(value)
    return max(variants, 1)


def parse_workflow(yaml_text: str) -> tuple[str, WorkflowFeatures]:
    try:
        data = yaml.safe_load(yaml_text)
    except yaml.YAMLError as exc:
        raise WorkflowParseError(f"Invalid workflow YAML: {exc}") from exc

    if not isinstance(data, dict):
        raise WorkflowParseError("Workflow YAML must parse to an object")

    workflow_name = str(data.get("name", "unnamed-workflow"))
    jobs = data.get("jobs", {})
    if not isinstance(jobs, dict) or not jobs:
        raise WorkflowParseError("Workflow requires at least one job")

    job_count = len(jobs)
    step_count = 0
    matrix_variants = 1
    uses_cache_step = False
    dependency_install_steps = 0

    for job in jobs.values():
        if not isinstance(job, dict):
            continue

        strategy = job.get("strategy", {})
        matrix_variants += _matrix_variants(strategy.get("matrix", {})) - 1

        for step in job.get("steps", []):
            if not isinstance(step, dict):
                continue
            step_count += 1

            uses = str(step.get("uses", "")).lower()
            run = str(step.get("run", "")).lower()
            if "actions/cache" in uses:
                uses_cache_step = True
            if any(keyword in run for keyword in ("npm ci", "pip install", "poetry install", "bundle install")):
                dependency_install_steps += 1

    features = WorkflowFeatures(
        jobs=job_count,
        steps=step_count,
        matrix_variants=matrix_variants,
        uses_cache_step=uses_cache_step,
        dependency_install_steps=dependency_install_steps,
    )
    return workflow_name, features
