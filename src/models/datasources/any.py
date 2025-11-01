#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

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
]

# ----------------------------------------------------------------
# EXPORTS
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
