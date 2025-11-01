#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Step containing main recursion
"""

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import logging

from datetime import timedelta
from datetime import datetime

from ...._core.logging import *
from ....models.application import *
from ....models.filesmanager import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "step_search_directory",
]

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------

@echo_function(
    tag="STEP - Perform recursive search on '{label}'",
    level="INFO",
    depth=0,
)
def step_search_directory(
    manager: FilesManager,
    /,
    *,
    path: str,
    max_depth: int,
    max_items: int,
    max_duration: timedelta,
):
    t = datetime.now()
    t_max = t + max_duration

    logging.warning("not yet implemented")

    folder = manager.get_folder(path)

    return
