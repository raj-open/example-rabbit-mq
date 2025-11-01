#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from functools import wraps
from typing import Callable
from typing import Generic
from typing import ParamSpec
from typing import TypeVar
from typing import Union

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "ExceptionWithData",
    "convert_notes_to_exception",
]

# ----------------------------------------------------------------
# LOCAL TYPES
# ----------------------------------------------------------------

PARAMS = ParamSpec("PARAMS")
JSON_TYPE_BASIC = Union[None, bool, str, int, float]
JSON_TYPE = Union[JSON_TYPE_BASIC, list[JSON_TYPE_BASIC], dict[str, JSON_TYPE_BASIC]]
NOTES = TypeVar("NOTES", bound=JSON_TYPE)

# ----------------------------------------------------------------
# CLASSES
# ----------------------------------------------------------------


class ExceptionWithData(Exception, Generic[NOTES]):
    """
    Generic error class with data
    """

    _data: dict[str, NOTES]

    def __init__(self, *_, **__):
        super(Exception, self).__init__(*_, **__)
        self._data = dict[str, NOTES]()

    @property
    def code(self) -> int | None:
        """
        Error code attached to exception
        """
        code = self.get_data("code")
        if isinstance(code, int):
            return int(code)
        return None

    @code.setter
    def code(self, x: int):
        """
        Attach error code to exception
        """
        self.add_data("code", None)
        if isinstance(x, int):
            self.add_data("code", x)

    @property
    def data(self) -> dict[str, NOTES]:
        """
        Data attached to exception
        """
        return self._data

    @data.setter
    def data(self, x: dict[str, NOTES], /):
        """
        Attach data to exception
        """
        self._data = x

    def get_data(
        self,
        key: str,
        /,
    ) -> NOTES:
        """
        Get value of data by key
        """
        return self._data.get(key)

    def add_data(
        self,
        key: str,
        value: NOTES,
        /,
    ):
        """
        Add data to exception
        """
        self._data.update({key: value})


# ----------------------------------------------------------------
# DECORATORS
# ----------------------------------------------------------------


def convert_notes_to_exception(
    method: Callable[PARAMS, dict[str, NOTES]],
    /,
):
    """
    Decorates a validation method, converting notes into exception-notes
    """

    @wraps(method)
    def wrapped_method(*_: PARAMS.args, **__: PARAMS.kwargs):
        notes = method(*_, **__)
        if len(notes) == 0:
            return

        err = ExceptionWithData[NOTES]("data invalid")
        err.data = notes
        raise err

    return wrapped_method
