"""CLI: python -m flakeline.run --suite sample --runs 10"""
import argparse
import json

from .runner import run_suite, find_flakes
from .client import diagnose_flake


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--suite", default="sample")
    ap.add_argument("--runs", type=int, default=10)
    args = ap.parse_args()

    outcomes = run_suite(args.suite, args.runs)
    flakes = find_flakes(outcomes)
    print(f"Ran {args.runs}x. {len(outcomes)} tests, {len(flakes)} flaky.")
    for test, obs in flakes.items():
        print(f"FLAKY {test}: {obs}")
        result = diagnose_flake(test, f"outcomes across runs: {obs}")
        print(json.dumps(result, indent=2)[:800])
    if not flakes:
        print("No flakes detected.")


if __name__ == "__main__":
    main()
