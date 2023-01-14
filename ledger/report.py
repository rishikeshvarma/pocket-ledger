from collections import defaultdict

from tabulate import tabulate


def totals_by_category(entries):
    totals = defaultdict(float)
    for e in entries:
        totals[e["category"]] += e["amount"]
    return dict(sorted(totals.items(), key=lambda kv: -kv[1]))


def category_table(entries, currency="Rs"):
    totals = totals_by_category(entries)
    rows = [(cat, f"{currency}{amt:,.2f}") for cat, amt in totals.items()]
    rows.append(("TOTAL", f"{currency}{sum(totals.values()):,.2f}"))
    # TODO: percentage of the month per category
    return tabulate(rows, headers=["category", "spent"])
