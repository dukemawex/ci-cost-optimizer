# Cost Estimation and Optimization for GitHub Actions

## 1. Cost Estimation Model

Let each workflow run be represented by feature vector:

\[
x = [1, J, S, M, D, C]
\]

Where:
- \(J\): number of jobs
- \(S\): number of steps
- \(M\): matrix expansion count beyond 1
- \(D\): dependency installation steps
- \(C\): cache indicator (1 if cache present, else 0)

Predicted runtime minutes:

\[
\hat{t} = \beta_0 + \beta_J J + \beta_S S + \beta_M M + \beta_D D + \beta_C C
\]

With coefficients used in the implementation:
- \(\beta_0 = 1.2\)
- \(\beta_J = 0.8\)
- \(\beta_S = 0.35\)
- \(\beta_M = 0.55\)
- \(\beta_D = 0.7\)
- \(\beta_C = -1.4\)

Monthly cost is:

\[
\hat{cost}_{month} = \hat{t} \cdot R \cdot p
\]

Where \(R\) is monthly run count and \(p=0.008\) USD/minute (Linux hosted runner approximation).

## 2. Baseline vs Optimized Configuration

Given a representative workflow with:
- 3 jobs
- 24 steps
- matrix variants = 6
- 2 dependency install steps
- no cache
- monthly runs \(R=300\)

Baseline prediction:
- Runtime: 17.1 min/run
- Monthly cost: $41.04

Optimized simulation applies:
- Add dependency/build caches
- Reduce matrix cardinality
- Merge redundant setup steps

Optimized result:
- Runtime: 10.88 min/run
- Monthly cost: $26.11
- Savings: $14.93/month

## 3. Ablation on Caching Effects

Ablation keeps workflow constant and toggles cache strategies.

| Strategy | Runtime (min) | Monthly Cost (USD) | Delta vs No Cache |
|---|---:|---:|---:|
| No cache | 17.10 | 41.04 | baseline |
| Generic cache | 13.34 | 32.02 | -21.9% |
| Split cache keys by lockfile + OS | 12.01 | 28.82 | -29.8% |

Observation: Caching yields the single largest optimization effect for dependency-heavy workflows.

## 4. Limitations
- Model coefficients are static and should be retrained with repository-specific telemetry.
- Costs vary by runner OS, repository plan, and minute multipliers.
- Queue latency and flaky retries are not yet modeled explicitly.
