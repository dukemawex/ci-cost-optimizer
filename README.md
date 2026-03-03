# ci-cost-optimizer

Cost prediction and optimization recommendation engine for GitHub Actions workflows.

## Features
- Parse GitHub Actions workflow YAML into runtime/cost features.
- Predict runtime with a lightweight regression-style model.
- Simulate caching and matrix optimization strategies.
- Estimate monthly GitHub Actions cost.
- Retrieve CI optimization references via Tavily (with offline fallback).
- Generate a structured recommendation memo via Gemini (with deterministic fallback).
- Persist required artifacts:
  - `artifacts/runs.json`
  - `artifacts/predictions.json`
  - `artifacts/optimization_plan.json`
  - `artifacts/sources.json`

## FastAPI Demo
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Analyze endpoint
`POST /analyze`

```json
{
  "workflow_yaml": "name: CI\non: [push]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - run: npm ci\n      - run: npm test",
  "monthly_runs": 300
}
```

### Environment variables
- `TAVILY_API_KEY` (optional): if set, live Tavily search is used.
- `GEMINI_API_KEY` (optional): if set, Gemini generates the recommendation memo.

## Project Structure
- `app/main.py`: FastAPI service.
- `engine/workflow_parser.py`: YAML parser + feature extraction.
- `engine/predictor.py`: runtime and cost estimation model.
- `engine/optimizer.py`: optimization simulation and plan builder.
- `engine/sources.py`: Tavily + authoritative source citations.
- `engine/memo.py`: Gemini integration.
- `engine/pipeline.py`: orchestration + artifact writing.
- `PAPER.md`: formal model and baseline-vs-optimized analysis.
