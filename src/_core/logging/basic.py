#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from __future__ import annotations

import json
import logging
import os
from logging import CRITICAL
from logging import DEBUG
from logging import ERROR
from logging import INFO
from logging import WARNING
from logging import FileHandler
from logging import Formatter
from logging import LogRecord
from logging import Logger
from logging import getLogger
from pathlib import Path
from typing import Any

from strip_ansi import strip_ansi

from .constants import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "configure_logging",
]

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def configure_logging(
    *,
    level: LOG_LEVELS | int = INFO,
    name: str | None = None,
    path: str | None = None,
    format_date: str = r"%Y-%m-%d %H:%M:%S",
    serialise: bool = True,
) -> Logger:
    """
    Establishes logging for console and files.
    """
    name = name or "root"
    fmt_console = "%(asctime)s $\x1b[92;1m%(name)s\x1b[0m [\x1b[1m%(levelname)s\x1b[0m] %(message)s"  # fmt: skip
    logging.basicConfig(format=fmt_console, datefmt=format_date, encoding="utf-8")
    logger = getLogger(name=name)
    if isinstance(level, str):
        level = logging.getLevelNamesMapping().get(level, INFO)
    logger.setLevel(level)

    if not isinstance(path, str):
        return

    if serialise:
        fmt = JsonFormatter(r"%(message)s")

    else:
        fmt = Formatter(fmt=strip_ansi(fmt_console), datefmt=format_date)

    for path_file, level in [
        (f"{path}/out.log", INFO),
        (f"{path}/out.log", WARNING),
        (f"{path}/err.log", ERROR),
        (f"{path}/err.log", CRITICAL),
        (f"{path}/debug.log", DEBUG),
    ]:
        create_file_if_not_exists(path_file)
        handler = FileHandler(path_file, encoding="utf-8")
        handler.setFormatter(fmt)
        handler.setLevel(level)
        handler.addFilter(LoggingLevelFilter(level))
        logger.addHandler(handler)

    return logger


# ----------------------------------------------------------------
# MAIN CLASSES + METHODS
# ----------------------------------------------------------------


class LoggingLevelFilter(logging.Filter):
    def __init__(self, logging_level: int):
        super().__init__()
        self.logging_level = logging_level

    def filter(self, record: LogRecord) -> bool:
        return record.levelno == self.logging_level


class JsonFormatter(Formatter):
    def format(self, record: LogRecord, /):
        """
        intercepts logging:

        - replaces message by entire record
        - filters to desired keys in the given order
        - serialises to a valid JSON if possible
        """
        # force universal path standard
        record.pathname = Path(record.pathname).as_posix()

        # make the record the entire message:
        parts = record.__dict__
        parts["message"] = parts.get("msg", None)
        parts = {key: parts.get(key, None) for key in REPORT_KEYS}

        # ensure proper JSON'ised message
        record.msg = serialise(parts)

        return super().format(record)


# ----------------------------------------------------------------
# AUXILIARY CLASSES + METHODS
# ----------------------------------------------------------------


def create_dir_if_not_exists(
    path: str,
    /,
):
    p = Path(path)
    if p.exists():
        return
    p.mkdir(parents=True, exist_ok=True)


def create_file_if_not_exists(
    path: str,
    /,
    *,
    rights: int = 0o664,
):
    """
    Creates a file if it does not already exist

    NOTE: Digits of `rights` define

    - digit 1: rights for user
    - digit 2: rights for group
    - digit 3: rights for others

    Each digit is an octal number 0-7 (think binary)

    | digit | binary | rights |
    | ----: | :----: | :----: |
    | 0     |   000  |  - - - |
    | 1     |   001  |  - - x |
    | 2     |   010  |  - w - |
    | 3     |   011  |  - w x |
    | 4     |   100  |  r - - |
    | 5     |   101  |  r - x |
    | 6     |   110  |  r w - |
    | 7     |   111  |  r w x |

    where

    - `r` = read access
    - `w` = write access
    - `x` = execution rights

    e.g. `0o664` means read+write for user and group,
    and read only for others.
    """
    create_dir_if_not_exists(os.path.dirname(path))
    p = Path(path)
    if p.exists():
        return
    p.touch(mode=rights, exist_ok=True)


def serialise(value: Any, /) -> str:
    """
    Safe jsonisation of a value if possible.
    Otherwise resorts to mere stringification.
    """
    try:
        return json.dumps(
            value,
            skipkeys=False,
            ensure_ascii=False,
            allow_nan=True,
            sort_keys=False,
        )

    except Exception as _:
        pass

    try:
        return str(value)

    except Exception as _:
        pass

    return None
