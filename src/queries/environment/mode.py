#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from .basic import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "get_path_logs",
]

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


@add_environment
def get_path_logs(
    # DEV-NOTE: from decorator
    path: str,
    env: dict[str, str],
    # end decorator args
) -> str | None:
    """
    Returns logging path set in environment
    """
    # NOTE: ensure that even the empty string is converted to null
    value = env.get("PATH_LOGS") or None
    return value
