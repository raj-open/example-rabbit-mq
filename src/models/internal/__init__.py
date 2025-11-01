#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This submodule provides the methods to be used in setup/config.py
"""

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from .decorators import *
from .errors import *
from .temp import *
from .traits import *
from .trees import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "ExceptionWithData",
    "GenericTree",
    "Property",
    "TempNameGenerator",
    "TriggerProperty",
    "convert_notes_to_exception",
    "mark_errors",
    "perform_action_on_error",
    "temp_name",
]
