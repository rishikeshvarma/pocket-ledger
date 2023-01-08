import json
import os
from datetime import datetime

DEFAULT_PATH = os.path.expanduser("~/.pocket-ledger.json")


class Ledger:
    def __init__(self, path=DEFAULT_PATH):
        self.path = path
        self.entries = []
        if os.path.exists(path):
            with open(path) as f:
                self.entries = json.load(f)

    def add(self, amount, category, note=""):
        entry = {
            "amount": round(float(amount), 2),
            "category": category.lower(),
            "note": note,
            "at": datetime.utcnow().isoformat(timespec="seconds"),
        }
        self.entries.append(entry)
        return entry

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.entries, f, indent=2)

    def total(self, category=None):
        return round(sum(e["amount"] for e in self.entries
                         if category is None or e["category"] == category.lower()), 2)
