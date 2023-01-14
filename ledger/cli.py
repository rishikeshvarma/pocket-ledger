import argparse
import sys

from ledger.report import category_table
from ledger.store import Ledger


def build_parser():
    p = argparse.ArgumentParser(prog="ledger", description="pocket-ledger: track daily expenses")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add", help="add an expense")
    a.add_argument("amount", type=float)
    a.add_argument("category")
    a.add_argument("note", nargs="?", default="")
    sub.add_parser("list", help="show every expense")
    sub.add_parser("total", help="totals per category")
    return p


def main(argv=None, ledger=None):
    args = build_parser().parse_args(argv)
    ledger = ledger or Ledger()
    if args.cmd == "add":
        e = ledger.add(args.amount, args.category, args.note)
        ledger.save()
        print(f"added {e['amount']} to {e['category']}")
    elif args.cmd == "list":
        for e in ledger.entries:
            print(f"{e['at']}  {e['category']:<12} {e['amount']:>8.2f}  {e['note']}")
    elif args.cmd == "total":
        print(category_table(ledger.entries))
    return 0


if __name__ == "__main__":
    sys.exit(main())
