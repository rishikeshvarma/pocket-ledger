import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from ledger.cli import main
from ledger.config import merge
from ledger.report import category_table, totals_by_category
from ledger.store import Ledger


class LedgerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ledger = Ledger(os.path.join(self.tmp.name, "ledger.json"))

    def tearDown(self):
        self.tmp.cleanup()

    def test_add_and_total(self):
        self.ledger.add(40, "Chai")
        self.ledger.add(120.5, "food", "biryani")
        self.assertEqual(self.ledger.total(), 160.5)
        self.assertEqual(self.ledger.total("chai"), 40)

    def test_save_and_reload(self):
        self.ledger.add(10, "bus")
        self.ledger.save()
        self.assertEqual(Ledger(self.ledger.path).total(), 10)

    def test_totals_by_category(self):
        entries = [{"amount": 5, "category": "a"}, {"amount": 7, "category": "b"},
                   {"amount": 1, "category": "a"}]
        self.assertEqual(totals_by_category(entries), {"b": 7, "a": 6})

    def test_category_table(self):
        out = category_table([{"amount": 99, "category": "chai"}], "Rs")
        self.assertIn("chai", out)
        self.assertIn("Rs99.00", out)

    def test_cli_add(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            main(["add", "30", "chai"], ledger=self.ledger)
        self.assertIn("added 30.0 to chai", buf.getvalue())

    def test_merge_nested(self):
        self.assertEqual(merge({"a": {"x": 1}}, {"a": {"y": 2}}), {"a": {"x": 1, "y": 2}})


if __name__ == "__main__":
    unittest.main()
