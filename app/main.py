from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from engine.pipeline import analyze_workflow
from engine.workflow_parser import WorkflowParseError

app = FastAPI(title="CI Cost Optimizer", version="0.1.0")


class AnalyzeRequest(BaseModel):
    workflow_yaml: str = Field(..., description="Raw GitHub Actions workflow YAML")
    monthly_runs: int = Field(300, ge=1, le=100000)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze")
def analyze(request: AnalyzeRequest) -> dict:
    try:
        return analyze_workflow(request.workflow_yaml, request.monthly_runs)
    except WorkflowParseError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
