from __future__ import annotations

from engine.models import OptimizationPlan, WorkflowFeatures


def simulate_caching_improvements(features: WorkflowFeatures, baseline_minutes: float) -> tuple[float, list[str]]:
    optimized = baseline_minutes
    improvements: list[str] = []

    if not features.uses_cache_step:
        optimized *= 0.78
        improvements.append("Add actions/cache for dependencies and build outputs.")
    elif features.dependency_install_steps > 1:
        optimized *= 0.9
        improvements.append("Refine cache keys and split dependency caches by ecosystem.")

    if features.matrix_variants > 4:
        optimized *= 0.88
        improvements.append("Reduce matrix cardinality to critical OS/runtime combinations.")

    if features.steps > 20:
        optimized *= 0.93
        improvements.append("Combine redundant setup/test steps and reuse composite actions.")

    return round(max(optimized, 0.8), 2), improvements


def build_recommendation_memo(
    features: WorkflowFeatures,
    baseline_minutes: float,
    baseline_monthly_cost: float,
    monthly_runs: int,
) -> OptimizationPlan:
    optimized_minutes, actions = simulate_caching_improvements(features, baseline_minutes)
    optimized_monthly_cost = round(optimized_minutes * monthly_runs * 0.008, 2)
    savings = round(baseline_monthly_cost - optimized_monthly_cost, 2)

    bottlenecks: list[str] = []
    if features.dependency_install_steps > 0:
        bottlenecks.append("Repeated dependency installation dominates wall-clock time.")
    if features.matrix_variants > 3:
        bottlenecks.append("Large matrix strategy multiplies execution minutes.")
    if features.steps > 18:
        bottlenecks.append("High step count increases setup overhead.")
    if not bottlenecks:
        bottlenecks.append("Moderate workflow complexity with incremental optimization opportunities.")

    if not actions:
        actions.append("Monitor cache hit rate and add targeted profiling to validate efficiency.")

    return OptimizationPlan(
        bottlenecks=bottlenecks,
        cost_savings_estimate=savings,
        action_plan=actions,
        optimized_minutes=optimized_minutes,
        optimized_monthly_cost_usd=optimized_monthly_cost,
    )
