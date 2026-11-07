from datetime import datetime, timezone

WARN_AT = 0.8


def this_month():
    """The current month as "YYYY-MM", in UTC like the saved timestamps."""
    return datetime.now(timezone.utc).strftime("%Y-%m")


def check_budgets(entries, budgets, month=None):
    """Compare this month's spending with each category's budget.

    Returns one line per budget: ok, a warning at 80% or more, or an alert at
    100% or more. Unused budget does not roll over to the next month.
    """
    month = month or this_month()
    spent = {}
    for e in entries:
        if str(e.get("at", "")).startswith(month):
            cat = e["category"].lower()
            spent[cat] = spent.get(cat, 0) + e["amount"]

    if not budgets:
        return ['no budgets set: add "budgets": {"food": 3000} to ~/.pocket-ledgerrc.json']

    lines = []
    for category, limit in sorted(budgets.items()):
        used = round(spent.get(category.lower(), 0), 2)
        if limit <= 0:
            lines.append(f"{category}: budget must be more than 0")
            continue
        share = used / limit
        status = f"{category}: {used:,.2f} of {limit:,.2f} ({share:.0%})"
        if share >= 1:
            lines.append(f"OVER BUDGET! {status}")
        elif share >= WARN_AT:
            lines.append(f"warning, nearly there: {status}")
        else:
            lines.append(f"ok: {status}")
    return lines
