"""Sample repo with a PLANTED flaky test (order-dependent shared state)."""
import os

_counter_file = os.path.join(os.path.dirname(__file__), ".counter")


def _count():
    try:
        with open(_counter_file) as f:
            n = int(f.read())
    except (FileNotFoundError, ValueError):
        n = 0
    with open(_counter_file, "w") as f:
        f.write(str(n + 1))
    return n


def test_stable_addition():
    assert 1 + 1 == 2


def test_planted_flake():
    """Fails on every 3rd run: shared counter file leaks state across runs."""
    n = _count()
    assert n % 3 != 2, f"planted flake fired on run count {n}"
