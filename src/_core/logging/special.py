#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import logging
import os
import sys
from pathlib import Path
from typing import Any
from typing import Callable
from typing import TypeVar

from .constants import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "log",
    "log_console",
    "log_debug_wrapped",
    "log_debug_wrapped_args",
    "log_dev",
]

# ----------------------------------------------------------------
# LOCAL CONSTANTS/VARIABLES
# ----------------------------------------------------------------

T = TypeVar("T")

# ----------------------------------------------------------------
# ENUM
# ----------------------------------------------------------------


def get_log_level(level: str | int, /) -> int:
    if isinstance(level, str):
        level = logging.getLevelNamesMapping().get(level, logging.INFO)
    return level


# ----------------------------------------------------------------
# METHODS - SPECIAL
# ----------------------------------------------------------------


def log_debug_wrapped(cb: Callable[[], str], /):
    """
    Performs logging.debug with the message is wrapped by a function call,
    which is only called if DEBUG-mode is active.

    NOTE: used to save processing time
    """
    if logging.DEBUG < logging.root.level:
        return
    message = cb()
    for text in message.split("\n"):
        logging.debug(text)


def log_debug_wrapped_args(
    msg: Any,
    *_,
    **__,
):
    """
    Performs logging.debug
    with the computation of the message wrapped by a function call,
    which is only called if DEBUG-mode is active.

    NOTE: used to save processing time
    """
    if logging.DEBUG < logging.root.level:
        return

    values = [str(value) for value in _]
    values += [f"{key}: {value}" for key, value in __.items()]  #  fmt: skip
    values_str = "; ".join(values)

    logging.debug(f"{msg} | {values_str}")


def log_console(*messages: Any):
    for text in messages:
        sys.stdout.write(f"{text}\n")
        sys.stdout.flush()


def log_dev(*messages: Any, path: str):  # pragma: no cover
    p = Path(path)
    if not p.exists():
        Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
        p.touch(mode=0o644)

    with open(path, "a", encoding="utf-8") as fp:
        print(*messages, file=fp)


# ----------------------------------------------------------------
# METHODS - UNIVERSAL
# ----------------------------------------------------------------


def log(
    *messages: Any,
    level: LOG_LEVELS | int | None = None,
):
    level = get_log_level(level)
    match level:
        case None:
            return log_console(*messages)

        case "DEBUG":
            for text in messages:
                logging.debug(text)

        case "WARN" | "WARNING":
            for text in messages:
                logging.warning(text)

        case "ERROR":
            for text in messages:
                logging.error(text)

        case "CRITICAL" | "FATAL":
            message = "\n".join([str(text) for text in messages])
            logging.fatal(message)
            exit(1)

        # case "INFO":
        case _:
            for text in messages:
                logging.info(text)
