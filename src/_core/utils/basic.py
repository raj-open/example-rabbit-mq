#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import json
import re
from datetime import datetime
from enum import Enum
from enum import StrEnum
from functools import reduce
from typing import Any
from typing import Callable
from typing import Iterable
from typing import Sequence
from typing import TypeVar
from typing import overload

from flatdict import FlatDict

from .code import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "as_flattened_dict",
    "coerce_null",
    "create_regex_from_prefix_pattern",
    "extract_string",
    "extract_strip",
    "first_non_null",
    "flatdict_to_dict",
    "flatten",
    "flatten_mixed",
    "flatten_sets",
    "indicator_function_factory",
    "json_deserialise",
    "merge_dicts",
    "safe_format_string",
    "split_string_list",
    "validate_regex",
]

# ----------------------------------------------------------------
# LOCAL CONSTANTS / VARIABLES
# ----------------------------------------------------------------

MAX_ITER = 1000

T = TypeVar("T")
_DATE_PATTERN = re.compile(pattern=r"^\d+-\d+-\d+$")
_TIME_PATTERN = re.compile(pattern=r"^\d+:\d+(:\d+(\.\d+)?)?$")

# ----------------------------------------------------------------
# METHODS - VALUES
# ----------------------------------------------------------------


def first_non_null(
    *values: T | None,
    default: T,
) -> T:
    for value in values:
        if value is None:
            continue
        return value
    return default


# ----------------------------------------------------------------
# METHODS - STRINGS
# ----------------------------------------------------------------


def safe_format_string(
    text: str,
    *pos_args: Any,
    **kwargs: Any,
) -> str:
    """
    Safely formats string leaving missing arguments alone.
    """
    n_pos = len(pos_args)
    for _ in range(MAX_ITER):
        try:
            return text.format(*pos_args, **kwargs)

        except IndexError as err:
            if n_pos == 0:
                text = re.sub(pattern="\\{\\}", repl="{{}}", string=text)
            text = re.sub(pattern=f"\\{{{n_pos}\\}}", repl=f"{{{{{n_pos}}}}}", string=text)
            n_pos += 1

        except KeyError as err:
            key = [*err.args, "?"][0]
            text = re.sub(pattern=f"\\{{{key}\\}}", repl=f"{{{{{key}}}}}", string=text)

    raise Exception(f"could not safely format '{text}'")


@overload
def extract_string(x: None, /) -> None: ...


@overload
def extract_string(x: str | StrEnum, /) -> str: ...


@overload
def extract_string(x: Sequence[str | StrEnum] | set[str | StrEnum], /) -> list[str]: ...


@overload
def extract_string(x: dict[str | StrEnum, str | StrEnum], /) -> dict[str, str]: ...


def extract_string(
    x: (
        None
        | str
        | StrEnum
        | Sequence[str | StrEnum]
        | set[str | StrEnum]
        | dict[str | StrEnum, str | StrEnum]
    ),
    /,
):  # -> None | str | list[str] | dict[str, str]:
    """
    Returns the underlying string value of a string or string-enum.

    - Converts string/enum to string
    - Converts list of strings/enums to list of strings
    - Converts dictionary of strings/enums to dictionary of strings
    """
    match x:
        case None:
            return None

        # DEV-NOTE: must prioritise Enum over str, since StrEnum extends str!
        case Enum():
            return x.value

        case str():
            return x

        case dict():
            return {extract_string(key): extract_string(value) for key, value in x.items() }  # fmt: skip

        case _:
            return [extract_string(xx) for xx in x]


def extract_strip(
    x: str | StrEnum,
    /,
    *,
    left: str | None = None,
    right: str | None = None,
) -> str:
    """
    Performs left/right-strip to a string or string enum.
    """
    x = extract_string(x)
    if left is not None:
        x = x.removeprefix(left)
    if right is not None:
        x = x.removesuffix(right)
    return x


def json_deserialise(x: str) -> Any:
    """
    Parses a JSON-ised string
    """
    # if parses normally, return this
    try:
        return json.loads(x)

    except Exception as err:
        pass

    # otherwise attempt to parse as time/date
    try:
        if re.match(pattern=_TIME_PATTERN, string=x):
            return datetime.fromisoformat(f"2000-01-01 {x}").time()

        elif re.match(pattern=_DATE_PATTERN, string=x):
            return datetime.fromisoformat(x).date()

        else:
            return datetime.fromisoformat(x)

    except Exception as err:
        pass

    raise Exception(f"failed to parse {x}")


def split_string_list(
    value: str | None,
    /,
    *,
    sep: str = ",",
    remove_empty: bool = True,
) -> list[str]:
    """
    Parses a (typically) comma-separated list of string as a list of strings,
    optionally removes empty values (default `true`).
    """
    if value is None:
        return []

    value = value.strip()
    if value == "":
        return []

    values: list[str] = re.split(pattern=sep, string=value or "")
    values = [x.strip() for x in values]
    if remove_empty:
        values = [x for x in values if x != ""]

    return values


@make_safe_none
def validate_regex(text: str, /) -> re.Pattern[str]:
    result = re.compile(text)
    return result


@make_safe_none
def substitute_regex(text: str, /) -> re.Pattern[str]:
    result = re.compile(text)
    return result


def create_regex_from_prefix_pattern(text: str | None, /) -> str | None:
    r"""
    Transforms strings that are not strict regex patterns
    into proper regex patterns, e.g.
    ```py
    assert create_regex_from_pattern("H-AB") == r"^H-AB\b.*"
    assert create_regex_from_pattern("H-AB*") == r"^H-AB\b.*"
    assert create_regex_from_pattern("H-AB*,R*") == r"^H-AB\b.*|R\b.*"
    assert create_regex_from_pattern("(H-AB,R)*") == r"^(H-AB|R)\b.*"
    ```
    NOTE: If the input is null or text containing just white space, returns null.
    """
    if not isinstance(text, str):
        return None

    # remove spaces
    text = re.sub(pattern=r"\s", repl="", string=text)

    # if the text just consisted of white space, return null
    if text == "":
        return None

    # if the text does not end in *, add it
    if not text.endswith("*"):
        text += "*"

    text = re.sub(pattern=r"\^", repl="", string=text)
    text = re.sub(pattern=r",", repl=r"|", string=text)
    # DEV-NOTE: unclear why, but the '\' needs to be escaped!
    text = re.sub(pattern=r"([^\.])\.?\*", repl=r"\1\\b.*", string=text)
    text = re.sub(pattern=r"^\.?\*", repl=r".*", string=text)

    if validate_regex(text) is None:
        return None

    return f"^({text})$"


def coerce_null(
    x: T | None,
    /,
    *,
    default: T,
) -> T:
    """
    Replaces value by a default if null
    """
    if x is None:
        x = default
    return x


# ----------------------------------------------------------------
# METHODS - FUNCTIONS
# ----------------------------------------------------------------


def indicator_function_factory(value: T) -> Callable[[T], bool]:
    """
    Returns a boolean-valued function
    that returns `true` <==> the given value is assumed.
    """

    def indicator_function(x: T) -> bool:
        return x == value

    return indicator_function


# ----------------------------------------------------------------
# METHODS - ARRAYS
# ----------------------------------------------------------------


def flatten(X: Iterable[list[T]], /) -> list[T]:
    X_flat = []
    for XX in X:
        X_flat.extend(XX)
    return X_flat


def flatten_sets(X: Iterable[set[T]], /) -> set[T]:
    X_flat = set([])
    for XX in X:
        X_flat = X_flat.union(XX)
    return X_flat


def flatten_mixed(X: Iterable[T | list[T]], /) -> list[T]:
    X_flat = []
    for XX in X:
        if isinstance(XX, list):
            X_flat.extend(XX)

        else:
            X_flat.append(XX)

    return X_flat


def merge_dicts(*objects: dict | FlatDict) -> dict:
    """
    Merges dictionaries just like `dict1 | dict2`,
    but prevents values being overwritten by None

    ```py
    x = {'height': 200, 'name': 'Bob', 'colour': 'red'}
    y = {'height': None, 'colour': 'blue', 'city': 'London'}

    # { 'height': None, 'name': 'Bob', 'colour': 'blue', 'city': 'London'}
    print(x | y)

    # { 'height': 200, 'name': 'Bob', 'colour': 'blue', 'city': 'London'}
    print(merge_dicts(x, y))
    ```
    """
    objects = map(
        # wipes out keys with None-values
        lambda x: {key: value for key, value in x.items() if value is not None},
        objects,
    )
    # join cleaned objects together
    result = reduce(lambda x, y: x | y, objects, {})
    return result


def flatdict_to_dict(object: FlatDict, /) -> dict:
    """
    Convert FlatDict to a flattened dictionary.
    """
    return {**object}


def as_flattened_dict(object: dict, /, *, delimiter: str = ":") -> dict:
    """
    Convert a dictionary to a flattened dictionary.
    """
    return flatdict_to_dict(FlatDict(object, delimiter=delimiter))
