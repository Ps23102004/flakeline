# Flakeline

An agent that hunts flaky tests — for the **Nebius x NVIDIA Global AI Hackathon** (Coding and Agentic Engineering track).

## What it does

1. **Run** a test suite K times (default 10) against a sample repo.
2. **Flag** tests whose pass/fail outcome is nondeterministic across runs.
3. **Diagnose** the cause class with NVIDIA's Nemotron model via **Nebius Token Factory** (OpenAI-compatible API).
4. **Write** a minimal reproducer plus a quarantine annotation, then **re-run** to confirm the flake is contained.

The demo is fully deterministic: the sample repo ships with a planted flaky test, so every run has something real to find.

## How Nebius and NVIDIA are used

- **Nebius Token Factory** serves the model (OpenAI-compatible base `https://api.tokenfactory.nebius.com/v1/`).
- **NVIDIA Nemotron** (`nvidia/Nemotron-3.5-Super-VL`) classifies the flake cause (timing, ordering, shared state, randomness, external dependency) and drafts the reproducer.
- Optional: web-search tool calls can be routed through Tavily (Best Use of Tavily kicker).

## Setup

```bash
pip install -r requirements.txt
export NEBIUS_API_KEY="your Token Factory key"   # from the Nebius AI Builder Program
python -m flakeline.run --suite sample --runs 10
```

Without `NEBIUS_API_KEY`, the runner still detects flakes; diagnosis reports "no key" instead of calling the model.

## Submission checklist (Nebius x NVIDIA)

- [x] Public repo, MIT license at top
- [ ] Working demo URL
- [ ] Public YouTube demo (<=3 min) showing Token Factory + Nemotron use
- [ ] README setup + Nebius/NVIDIA usage (this file)
- [ ] Product feedback on the tools
- [ ] Submit by Thu Oct 30, 2026, 1:00pm EDT

## Why this is distinct

Flakeline hunts nondeterminism in test suites. It sits in the testing-tool neighborhood of the author's other work (Focus Auditor, Patch Cross-Examiner) but solves a different problem: flaky tests, not accessibility or patch correctness.
