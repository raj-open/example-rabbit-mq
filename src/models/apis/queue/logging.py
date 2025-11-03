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
    "RABBIT_LOG_LEVEL_ERROR",
    "RABBIT_LOG_LEVEL_INFO",
    "RABBIT_LOG_LEVEL_WARNING",
    "RABBIT_ROUTE_ERROR",
    "RABBIT_ROUTE_INFO",
    "RABBIT_ROUTE_WARNING",
]

# ----------------------------------------------------------------
# CONSTANTS
# ----------------------------------------------------------------

RABBIT_ROUTE_INFO = "[INFO]"
RABBIT_ROUTE_ERROR = "[ERROR]"
RABBIT_ROUTE_WARNING = "[WARNING]"
RABBIT_LOG_LEVEL_INFO = BasicProperties(type="info", priority=1)
RABBIT_LOG_LEVEL_WARNING = BasicProperties(type="warning", priority=10)
RABBIT_LOG_LEVEL_ERROR = BasicProperties(type="error", priority=100)
