#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module contains methods for setup purposes,
e.g. configuration of application.
"""

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

# NOTE: only import/export the submodules which are called as such
from . import config
from .config import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "INFO",
    "TIMEZONE",
    "VERSION",
    "config",
]
