#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from pika import BasicProperties

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "RABBIG_LOG_LEVEL_ERROR",
    "RABBIG_LOG_LEVEL_INFO",
    "RABBIG_LOG_LEVEL_WARNING",
]

# ----------------------------------------------------------------
# CONSTANTS
# ----------------------------------------------------------------

RABBIG_LOG_LEVEL_INFO = BasicProperties(type="info", priority=1)
RABBIG_LOG_LEVEL_WARNING = BasicProperties(type="warning", priority=10)
RABBIG_LOG_LEVEL_ERROR = BasicProperties(type="error", priority=100)
