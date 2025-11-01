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
) -> str:
    value = env.get("PATH_LOGS", ".session")
    return value
