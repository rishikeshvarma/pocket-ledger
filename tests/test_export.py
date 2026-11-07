import csv
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from ledger.cli import main
from ledger.store import Ledger


class ExportTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.ledger = Ledger(os.path.join(self.tmp.name, "ledger.json"))
        self.ledger.add(40, "chai", "with, a comma")
        self.ledger.add(180, "food", "=HYPERLINK(1)")

    def test_export_to_a_file(self):
        path = os.path.join(self.tmp.name, "out.csv")
        with redirect_stdout(io.StringIO()):
            main(["export", "--csv", path], ledger=self.ledger)
        with open(path, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual([r["category"] for r in rows], ["chai", "food"])
        self.assertEqual(rows[0]["note"], "with, a comma")
        self.assertEqual(rows[0]["amount"], "40.0")

    def test_formula_like_notes_are_defused(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            main(["export"], ledger=self.ledger)
        rows = list(csv.DictReader(io.StringIO(buf.getvalue())))
        self.assertEqual(rows[1]["note"], "'=HYPERLINK(1)")

    def test_budget_command_no_longer_crashes(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            main(["budget"], ledger=self.ledger)
        self.assertTrue(buf.getvalue().strip())


if __name__ == "__main__":
    unittest.main()
