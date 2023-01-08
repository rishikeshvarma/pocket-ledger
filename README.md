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

## Plans

Monthly budgets per category, warnings when I am about to blow one, a CSV
export for my parents, and maybe a small chart of where the money goes each
month. Run the tests with `python -m unittest`.
