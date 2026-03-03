from fastapi.testclient import TestClient

from app.main import app
from engine.pipeline import analyze_workflow

SAMPLE = """
name: CI
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [\"3.10\", \"3.11\"]
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements.txt
      - run: pytest
"""


def test_pipeline_generates_expected_payload():
    result = analyze_workflow(SAMPLE, monthly_runs=200)
    assert result["workflow_name"] == "CI"
    assert result["estimated_monthly_cost_usd"] > result["optimized_monthly_cost_usd"]
    assert "bottlenecks" in result["recommendations"]


def test_api_analyze_endpoint():
    client = TestClient(app)
    response = client.post("/analyze", json={"workflow_yaml": SAMPLE, "monthly_runs": 120})
    assert response.status_code == 200
    body = response.json()
    assert "recommendations" in body
    assert body["predicted_runtime_minutes"] > 0
