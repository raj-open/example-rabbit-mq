#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import os
import re
from pathlib import Path

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "get_module",
    "get_root_path",
    "get_source_path",
    "get_this_module",
]

# ----------------------------------------------------------------
# CONSTANTS
# ----------------------------------------------------------------

_source = Path(__file__).parent.as_posix()
_root = Path(__file__).parent.parent.as_posix()

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def get_path(root: str, *parts: str) -> str:
    return root if len(parts) == 0 else Path(root, *parts).as_posix()


def get_root_path(*parts: str) -> str:
    return get_path(_root, *parts)


def get_source_path(*parts: str) -> str:
    return get_path(_source, *parts)


def get_this_module(path: str, /) -> str:
    """
    Returns the module equivalent of current path
    """
    # remove extension
    path, _ = os.path.splitext(path)
    # get parts
    rel = Path(path).relative_to(_root)
    parts = list(rel.parts)
    # join to form module name
    name = ".".join(parts)
    return name


def get_module(
    path: str,
    /,
    *,
    root: str = "src",
    prefix: str = r"^mocks?_(.*)",
    basename: str | None = None,
) -> str:
    """
    Replaces path to current mock-file by corresponding unmocked file
    """
    # remove extension
    path, _ = os.path.splitext(path)
    # get parts
    rel = Path(path).relative_to(_source)
    parts = list(rel.parts)
    # optionally replace final part
    if (basename or "") != "":
        parts[-1] = basename
    # remove test-prefixes
    parts = [re.sub(pattern=prefix, repl=r"\1", string=part) for part in parts]
    # join to form module name
    name = ".".join([root, *parts])
    return name
