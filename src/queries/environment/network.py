#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import json
from typing import Any

from .basic import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "get_shared_network",
]

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


@add_environment
def get_shared_network(
    # DEV-NOTE: from decorator
    path: str,
    env: dict[str, Any],
    # end decorator args
) -> bool:
    """
    Gets http password.
    If value not set in .env, will raise a (Key)Exception.
    """
    raw = env["SHARED_NETWORK"]
    value = json.loads(raw)
    value = bool(value)
    return value
