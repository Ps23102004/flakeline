"""Run a pytest suite K times, flag nondeterministic tests."""
import json
import subprocess
import sys
from collections import defaultdict


def run_suite(path, runs=10):
    """Return {test_id: [pass/fail per run]} for every test collected."""
    outcomes = defaultdict(list)
    for _ in range(runs):
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", path, "-v", "--tb=line"],
            capture_output=True, text=True)
        seen = set()
        for line in proc.stdout.splitlines():
            if "::" in line and (" PASSED" in line or " FAILED" in line):
                node = line.split()[0]
                outcomes[node].append("PASSED" in line)
                seen.add(node)
        for node in list(outcomes):
            if node not in seen and len(outcomes[node]) < runs:
                outcomes[node].append(None)  # not collected this run
    return outcomes


def find_flakes(outcomes):
    """Tests with both passes and failures across runs."""
    return {t: o for t, o in outcomes.items()
            if any(x is True for x in o) and any(x is False for x in o)}
