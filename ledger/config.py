import json
import os
from collections.abc import Mapping

CONFIG_PATH = os.path.expanduser("~/.pocket-ledgerrc.json")
DEFAULTS = {"currency": "Rs", "path": os.path.expanduser("~/.pocket-ledger.json"), "budgets": {}}


def merge(base, override):
    """Deep-merge the user's config over the defaults."""
    out = dict(base)
    for key, value in override.items():
        if isinstance(value, Mapping) and isinstance(out.get(key), Mapping):
            out[key] = merge(out[key], value)
        else:
            out[key] = value
    return out


def load_config(path=CONFIG_PATH):
    if not os.path.exists(path):
        return dict(DEFAULTS)
    with open(path) as f:
        return merge(DEFAULTS, json.load(f))
