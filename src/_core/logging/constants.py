#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from typing import Literal

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "LOG_LEVELS",
    "REPORT_KEYS",
]

# ----------------------------------------------------------------
# CONSTANTS/VARIABLES
# ----------------------------------------------------------------

REPORT_KEYS = [
    "asctime",
    "levelname",
    # "levelno",
    "name",
    # "msg",
    "message",
    # "args",
    "pathname",
    # "filename",
    "module",
    "lineno",
    "funcName",
    # "exc_info",
    # "exc_text",
    # "stack_info",
    "created",
    "relativeCreated",
    "msecs",
    "thread",
    "threadName",
    "processName",
    "process",
]

LOG_LEVELS = Literal[
    "DEBUG",
    "INFO",
    # "WARN",
    "WARNING",
    "ERROR",
    # "CRITICAL",
    "FATAL",
]
