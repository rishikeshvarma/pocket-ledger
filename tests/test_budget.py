import unittest
from unittest import mock

from ledger import budget
from ledger.budget import check_budgets


def entry(amount, category, at):
    return {"amount": amount, "category": category, "note": "", "at": at}


class BudgetTest(unittest.TestCase):
    def test_only_this_month_counts(self):
        entries = [entry(500, "food", "2026-11-02T10:00:00"), entry(900, "food", "2026-10-30T10:00:00")]
        self.assertEqual(check_budgets(entries, {"food": 1000}, month="2026-11"),
                         ["ok: food: 500.00 of 1,000.00 (50%)"])

    def test_warns_at_80_percent(self):
        lines = check_budgets([entry(800, "food", "2026-11-02T10:00:00")], {"food": 1000}, month="2026-11")
        self.assertTrue(lines[0].startswith("warning"))

    def test_shouts_at_100_percent(self):
        lines = check_budgets([entry(1000, "food", "2026-11-02T10:00:00")], {"food": 1000}, month="2026-11")
        self.assertTrue(lines[0].startswith("OVER BUDGET!"))

    def test_category_case_does_not_matter(self):
        lines = check_budgets([entry(100, "chai", "2026-11-02T10:00:00")], {"Chai": 200}, month="2026-11")
        self.assertIn("100.00 of 200.00", lines[0])

    def test_no_budgets_explains_how_to_add_one(self):
        self.assertIn("no budgets set", check_budgets([], {}, month="2026-11")[0])

    def test_zero_budget_is_reported_not_a_crash(self):
        self.assertIn("more than 0", check_budgets([], {"food": 0}, month="2026-11")[0])

    def test_defaults_to_the_current_month(self):
        with mock.patch.object(budget, "this_month", return_value="2026-11"):
            lines = check_budgets([entry(10, "bus", "2026-11-01T00:00:00")], {"bus": 100})
        self.assertIn("10.00 of 100.00", lines[0])


if __name__ == "__main__":
    unittest.main()
