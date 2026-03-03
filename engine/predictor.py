from __future__ import annotations

from engine.models import WorkflowFeatures

# Simple linear regression coefficients fit to synthetic historical CI runs.
INTERCEPT = 1.2
COEFFICIENTS = {
    "jobs": 0.8,
    "steps": 0.35,
    "matrix_variants": 0.55,
    "dependency_install_steps": 0.7,
    "cache_bonus": -1.4,
}

GITHUB_ACTIONS_RATE_PER_MINUTE = 0.008  # approximate hosted Linux cost


def predict_runtime_minutes(features: WorkflowFeatures) -> float:
    minutes = (
        INTERCEPT
        + COEFFICIENTS["jobs"] * features.jobs
        + COEFFICIENTS["steps"] * features.steps
        + COEFFICIENTS["matrix_variants"] * (features.matrix_variants - 1)
        + COEFFICIENTS["dependency_install_steps"] * features.dependency_install_steps
    )
    if features.uses_cache_step:
        minutes += COEFFICIENTS["cache_bonus"]
    return round(max(minutes, 1.0), 2)


def estimate_monthly_cost(predicted_minutes: float, monthly_runs: int) -> float:
    return round(predicted_minutes * monthly_runs * GITHUB_ACTIONS_RATE_PER_MINUTE, 2)
