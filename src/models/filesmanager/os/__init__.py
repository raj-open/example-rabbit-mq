#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This submodule provides a realisation of the FilesManager interface for local operating system
"""

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from .classes import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "OSFilesManager",
    "OSFilesManagerFile",
    "OSFilesManagerFolder",
]
