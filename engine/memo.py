from __future__ import annotations

import json
import os
from typing import Any

import requests


def generate_memo_with_gemini(default_memo: dict[str, Any]) -> dict[str, Any]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return default_memo

    prompt = (
        "You are a CI optimization assistant. Return strict JSON with keys "
        "bottlenecks (array of strings), cost_savings_estimate (number), action_plan (array of strings). "
        f"Base context: {json.dumps(default_memo)}"
    )

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-1.5-flash:generateContent?key={api_key}"
    )

    try:
        response = requests.post(
            url,
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=20,
        )
        response.raise_for_status()
        text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        parsed = json.loads(text)
        if {"bottlenecks", "cost_savings_estimate", "action_plan"}.issubset(parsed):
            return parsed
    except Exception:
        return default_memo

    return default_memo
