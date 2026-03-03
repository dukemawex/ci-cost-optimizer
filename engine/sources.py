from __future__ import annotations

import os
from typing import Any

import requests

TAVILY_URL = "https://api.tavily.com/search"

FALLBACK_SOURCES = [
    {
        "title": "GitHub Actions billing documentation",
        "url": "https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions",
        "snippet": "Official GitHub pricing model with included minutes and OS-specific multipliers.",
    },
    {
        "title": "Dependency caching reference",
        "url": "https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows",
        "snippet": "Authoritative guidance for cache keys and restore behavior.",
    },
    {
        "title": "GitHub-hosted runners reference",
        "url": "https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners",
        "snippet": "Runner specs that influence performance and execution duration.",
    },
]


def fetch_ci_sources(query: str = "GitHub Actions optimization caching billing") -> list[dict[str, Any]]:
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return FALLBACK_SOURCES

    try:
        response = requests.post(
            TAVILY_URL,
            json={"api_key": api_key, "query": query, "max_results": 5},
            timeout=15,
        )
        response.raise_for_status()
        payload = response.json()
        results = payload.get("results", [])
        cleaned = [
            {"title": item.get("title"), "url": item.get("url"), "snippet": item.get("content")}
            for item in results
        ]
        return cleaned or FALLBACK_SOURCES
    except Exception:
        return FALLBACK_SOURCES
