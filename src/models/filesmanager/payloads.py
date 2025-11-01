#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------


from functools import wraps
from typing import Callable
from typing import Concatenate
from typing import Generic
from typing import ParamSpec
from typing import TypeVar

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import SkipValidation

from ..._core.constants import *
from ..._core.utils.io import *
from ..generated.application import EnumDataFileFormat
from ..generated.application import EnumFilesSystem
from .config import *
from .traits import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "PayloadParser",
]

# ----------------------------------------------------------------
# CONSTANTS
# ----------------------------------------------------------------

T = TypeVar("T")
PARAMS = ParamSpec("PARAMS")
MODEL = TypeVar("MODEL")
RETURN = TypeVar("RETURN")

# ----------------------------------------------------------------
# CLASSES
# ----------------------------------------------------------------


class PayloadParser(BaseModel, Generic[T]):
    """
    Provides a method to parse payloads e.g. in endpoints.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    type_: type[BaseModel]
    managers: dict[EnumFilesSystem, SkipValidation[FilesManager]]
    location: EnumFilesSystem | None = None
    root: str | None = None

    def parse(
        self,
        contents: bytes | T | None = None,
        /,
        *,
        format: BASIC_FILETYPES | None = None,
    ) -> T:
        """
        Computes the payload for task insertion. There are 3 cases:

        - `contents ~ <PAYLOAD_TYPE>` -> returns this
        - `contents = null`  -> reads from local file in setup/...
        - `contents ~ bytes` -> parses payload.
        """
        managers = self.managers
        loc = self.location
        root = self.root

        try:
            fmt = EnumDataFileFormat(format)

        except Exception as _:
            fmt = None

        match contents:
            case BaseModel():
                assert isinstance(contents, self.type_)
                return contents

            case None:
                assert (loc is not None) and (root is not None), \
                    f"need to set location and path in PayloadParser for {self.type_.__name__}"  # fmt: skip
                loader = ConfigLoader[T](managers=managers, type_=self.type_)
                result = loader.load_from_file(loc=loc, path=root, fmt=fmt)
                return result

            case _:
                fmt = fmt or EnumDataFileFormat.FIELD_JSON
                loader = ConfigLoader[T](managers=managers, type_=self.type_)
                result = loader.load_from_contents(contents, fmt=fmt)
                return result

    def add_config_from_path(
        self,
        action: Callable[Concatenate[MODEL, PARAMS], RETURN],
        /,
    ):
        """
        Decorates method by adding config to it.

        NOTE: Only works for if obtaining configs from a path.
        """

        @wraps(action)
        def wrapped_action(*_: PARAMS.args, **__: PARAMS.kwargs) -> RETURN:
            cfg = self.parse()
            result = action(cfg, *_, *__)
            return result

        return wrapped_action
