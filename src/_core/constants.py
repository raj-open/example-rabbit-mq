#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from enum import StrEnum
from typing import Literal

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "BASIC_FILETYPES",
    "ENCODING",
    "MAP_MIME_TYPE_TO_FILETYPE",
    "MIME_TYPES",
    "SIZE_1_KB",
    "SIZE_1_MB",
    "EnumMimeTypes",
]

# ----------------------------------------------------------------
# CONSTANTS
# ----------------------------------------------------------------

SIZE_1_KB = 2**10
SIZE_1_MB = 2**20

ENCODING = Literal[
    "ascii",
    "utf-8",
    "utf-8-sig",
    "unicode_escape",
]

BASIC_FILETYPES = Literal[
    ".json",
    ".yaml",
    ".toml",
    ".xml",
    ".parquet",
    ".csv",
    ".xlsx",
]


class EnumMimeTypes(StrEnum):
    BYTES = "application/octet-stream"
    TEXT = "text/plain"
    JSON = "application/json"
    # see https://learn.microsoft.com/previous-versions/office/office-2007-resource-kit/ee309278(v=office.12)
    XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    YAML = "application/x-yaml"


MIME_TYPES = Literal[
    "application/octet-stream",
    "text/plain",
    "application/json",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/x-yaml",
]


MAP_MIME_TYPE_TO_FILETYPE: dict[MIME_TYPES, BASIC_FILETYPES] = {
    "application/x-yaml": ".yaml",
    "application/json": ".json",
}
