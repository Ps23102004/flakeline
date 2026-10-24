"""Minimal OpenAI-compatible client for Nebius Token Factory."""
import os
import requests

BASE_URL = "https://api.tokenfactory.nebius.com/v1"
DEFAULT_MODEL = "nvidia/Nemotron-3.5-Super-VL"


def diagnose_flake(test_name, failure_log, model=DEFAULT_MODEL, api_key=None):
    """Ask Nemotron to classify a flake's cause class and draft a reproducer.

    Returns a dict with cause_class, reasoning, and reproducer, or
    {"error": "no_api_key"} when NEBIUS_API_KEY is not set.
    """
    key = api_key or os.environ.get("NEBIUS_API_KEY")
    if not key:
        return {"error": "no_api_key",
                "hint": "Set NEBIUS_API_KEY from the Nebius AI Builder Program (Token Factory)."}
    prompt = (
        "You are a test-reliability expert. A test failed nondeterministically.\n"
        f"Test: {test_name}\nFailure log:\n{failure_log}\n\n"
        "Classify the cause into exactly one of: timing, ordering, shared-state, "
        "randomness, external-dependency, unknown. Then write a minimal reproducer "
        "and a one-line quarantine annotation. Reply in JSON with keys "
        "cause_class, reasoning, reproducer, quarantine."
    )
    resp = requests.post(
        f"{BASE_URL}/chat/completions",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"model": model,
              "messages": [{"role": "user", "content": prompt}],
              "temperature": 0.2},
        timeout=120,
    )
    resp.raise_for_status()
    return {"raw": resp.json()["choices"][0]["message"]["content"]}
