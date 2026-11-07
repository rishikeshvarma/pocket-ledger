# pocket-ledger

A tiny command-line expense tracker, because my UPI history is a mess and
every budgeting app wants a subscription. You add what you spend with one
command, and it keeps everything in a single JSON file in your home folder,
so there is no account, no sync and nothing to break.

## Usage

    python -m ledger.cli add 40 chai
    python -m ledger.cli add 180 food "biryani with the gang"
    python -m ledger.cli list
    python -m ledger.cli total
    python -m ledger.cli budget
    python -m ledger.cli export --csv spending.csv

Needs Python 3.10 or newer: `pip install -r requirements.txt`.

## Budgets

Put monthly budgets per category in `~/.pocket-ledgerrc.json`:

    {"budgets": {"food": 3000, "chai": 500}}

`budget` counts only this month (in UTC, like the saved times). It says
"warning" at 80% of a budget and "OVER BUDGET!" at 100%. Unused budget does
not roll over.

## Export

`export --csv FILE` writes every expense as CSV for a spreadsheet; leave out
`--csv` to print it. Notes that start with `=`, `+`, `-` or `@` get a `'` in
front, so spreadsheets do not run them as formulas.

## Plans

Maybe a small chart of where the money goes each month, and rolling unused
budget over to the next month. Run the tests with `python -m unittest`.
