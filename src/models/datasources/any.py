#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import json
from typing import Any

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import RootModel

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "AnyArray",
    "AnyDataFrame",
    "AnyDictionary",
    "AnyEntity",
    "serialise_any_element",
]

# ----------------------------------------------------------------
# CLASSES
# ----------------------------------------------------------------


class AnyEntity(BaseModel):
    """
    Dummy model for parsing any entity
    """

    model_config = ConfigDict(
        use_enum_values=True,
    )

    value: Any


class AnyDictionary(BaseModel):
    """
    Dummy model for parsing dictionaries
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
        use_enum_values=True,
    )


class AnyArray(RootModel[list[BaseModel]]):
    """
    Dummy model for parsing arrays
    """

    model_config = ConfigDict(
        use_enum_values=True,
    )

    root: list[Any]


class AnyDataFrame(RootModel[list[AnyDictionary]]):
    """
    Structure of tasks requests.yaml configuration file.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
    )
    root: list[AnyDictionary]


# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def serialise_any_element(x: Any, /) -> bytes:
    """
    Uses pydantic classes to as cleanly as possible JSON-serialise any element.
    """
    match x:
        case list():
            x = AnyArray(root=x)

        case dict():
            x = AnyDictionary(root=x)

    if isinstance(x, BaseModel):
        contents = x.model_dump_json(
            by_alias=True,
            exclude_none=True,
            exclude_unset=False,
            exclude_defaults=False,
            warnings="none",
        ).encode()
        return contents

    try:
        contents = json.dumps(x).encode()
        return contents

    except Exception as _:
        pass

    contents = str(x).encode()
    return contents
