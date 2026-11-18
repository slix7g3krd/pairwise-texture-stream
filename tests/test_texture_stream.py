import pytest
from render import texture_stream as mod

CASES = [
    ("delay_two", "m.feedback_delay(10, 8) == 2"),
    ("delay_zero", "m.feedback_delay(8, 10) == 0"),
    ("priority_coverage", "m.priority(0.9, 10.0, 1.0) > m.priority(0.1, 10.0, 1.0)"),
    ("priority_distance", "m.priority(0.5, 100.0, 1.0) < m.priority(0.5, 10.0, 1.0)"),
    ("budget_limit", "sum(m.byte_budget([10, 20, 30], 50)) <= 50"),
    ("budget_zero", "m.byte_budget([10, 20], 0) == []"),
    ("lock_true", "m.lock_page(3, {3}) is True"),
    ("lock_false", "m.lock_page(3, {1}) is False"),
    ("fallback_low", "m.fallback_mip(4, 3) == 2"),
    ("fallback_keep", "m.fallback_mip(2, 5) == 2"),
    ("billing_disjoint", "len(m.dedupe_billing({1, 2}, {3, 4, 5})) == 5"),
    ("billing_overlap", "len(m.dedupe_billing({1, 2}, {2, 3})) == 3"),
    ("billing_empty", "len(m.dedupe_billing(set(), set())) == 0"),
    ("priority_zero", "m.priority(0.0, 10.0, 1.0) == approx(0.0)"),
    ("format_srgb", "m.format_budget('srgb', 100) != m.format_budget('linear', 100)")
]

@pytest.mark.parametrize("name,expr", CASES, ids=[c[0] for c in CASES])
def test_contract(name, expr):
    assert eval(expr, {"m": mod, "approx": pytest.approx})
