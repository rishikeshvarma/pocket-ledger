import argparse
import sys
from distutils.util import strtobool

from ledger.budget import check_budgets
from ledger.config import load_config
from ledger.report import category_table
from ledger.store import Ledger


def confirm(question):
    answer = input(f"{question} [y/N] ").strip() or "n"
    return bool(strtobool(answer))


def build_parser():
    p = argparse.ArgumentParser(prog="ledger", description="pocket-ledger: track daily expenses")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add", help="add an expense")
    a.add_argument("amount", type=float)
    a.add_argument("category")
    a.add_argument("note", nargs="?", default="")
    sub.add_parser("list", help="show every expense")
    sub.add_parser("total", help="totals per category")
    c = sub.add_parser("clear", help="delete every expense")
    c.add_argument("--yes", action="store_true")
    sub.add_parser("budget", help="how this month compares with your budgets")
    # TODO: export --csv for my parents
    return p


def main(argv=None, ledger=None):
    args = build_parser().parse_args(argv)
    cfg = load_config()
    ledger = ledger or Ledger(cfg["path"])
    if args.cmd == "add":
        e = ledger.add(args.amount, args.category, args.note)
        ledger.save()
        print(f"added {e['amount']} to {e['category']}")
    elif args.cmd == "list":
        for e in ledger.entries:
            print(f"{e['at']}  {e['category']:<12} {e['amount']:>8.2f}  {e['note']}")
    elif args.cmd == "total":
        print(category_table(ledger.entries, cfg["currency"]))
    elif args.cmd == "clear":
        if args.yes or confirm("Delete every expense?"):
            ledger.entries = []
            ledger.save()
            print("cleared")
    elif args.cmd == "budget":
        # TODO: print a nice table instead of raw lines
        for line in check_budgets(ledger.entries, cfg.get("budgets", {})):
            print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
