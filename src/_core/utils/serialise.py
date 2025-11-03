#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import json
from datetime import datetime
from typing import Any

from pydantic import BaseModel
from safetywrap import Err
from safetywrap import Ok
from safetywrap import Result

from .any import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "JSON_TYPE",
    "JSON_TYPE_BASIC",
    "serialise_any_as_object",
    "serialise_any_as_text",
]

# ----------------------------------------------------------------
# TYPES
# ----------------------------------------------------------------

# NOTE: although datetime is not a primitive JSON type it can be used in code
JSON_TYPE_BASIC = None | bool | str | int | float | datetime
JSON_TYPE = JSON_TYPE_BASIC | list["JSON_TYPE"] | dict[str, "JSON_TYPE"]

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def serialise_any_as_object(x: Any, /) -> Result[JSON_TYPE, None]:
    """
    Converts any element to a JSON-serialisable object.

    NOTE: uses safety wrapping
    """
    # preprocess bytes + all complex JSON-types
    match x:
        case bytes():
            obj = x.decode()

        case list():
            obj = AnyArray(root=x)

        case dict():
            obj = AnyDictionary(root=x)

        case _:
            obj = x

    match obj:
        # cover base JSON-types + datetime
        case None | bool() | str() | int() | float() | datetime():
            return Ok(obj)

        # cover all complex JSON-types - use pydantic's serialisation
        case BaseModel():
            obj = obj.model_dump(
                mode="json",
                by_alias=True,
                exclude_none=True,
                exclude_unset=False,
                exclude_defaults=False,
                warnings="none",
            )

            # NOTE: collapse "root" if result is {"root": ...}
            if isinstance(obj, dict) and list(obj.keys()) == ["root"]:
                obj = obj.get("root", obj)

            return Ok(obj)

    raise Err(None)


def serialise_any_as_text(x: Any, /) -> Result[str, None]:
    """
    Serialises any element to a JSON text.

    NOTE: uses safety wrapping
    """
    obj = serialise_any_as_object(x)
    if isinstance(obj, Err):
        return Err(None)

    obj = obj.unwrap()

    # attempt JSON-serialisation
    try:
        text = json.dumps(
            obj,
            skipkeys=False,
            ensure_ascii=False,
            allow_nan=True,
            sort_keys=False,
        )
        return Ok(text)

    except Exception as _:
        pass

    # otherwise attempt to convert original object to string
    try:
        text = str(x)
        return Ok(text)

    except Exception as _:
        pass

    # otherwise fail
    return Err(None)
