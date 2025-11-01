#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from functools import wraps
from typing import Callable
from typing import Concatenate
from typing import ParamSpec
from typing import TypeVar

from ..._core.logging import *
from .traits import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "mark_errors",
    "perform_action_on_error",
]

# ----------------------------------------------------------------
# LOCAL CONSTANTS
# ----------------------------------------------------------------

RETURN = TypeVar("RETURN")
T = TypeVar("T")
PARAMS = ParamSpec("PARAMS")

# ----------------------------------------------------------------
# CLASSES
# ----------------------------------------------------------------


def mark_errors(has_error: TriggerProperty, /):
    """
    Decorates method by intercepting and marking Exceptions.
    """

    def dec(method: Callable[PARAMS, RETURN]) -> Callable[PARAMS, RETURN]:
        @wraps(method)
        def wrapped_method(*_: PARAMS.args, **__: PARAMS.kwargs) -> RETURN:
            try:
                value = method(*_, **__)
                return value

            except Exception as err:
                has_error.set()
                log_debug_wrapped_args(err, *_, **__)
                raise err

        return wrapped_method

    return dec


def perform_action_on_error(
    action: Callable[Concatenate[Exception, PARAMS], None],
):
    """
    Decorates method by intercepting and marking Exceptions.
    If an exception occurs, performs action, then raises error.
    """

    def dec(method: Callable[PARAMS, RETURN]) -> Callable[PARAMS, RETURN]:
        @wraps(method)
        def wrapped_method(*_: PARAMS.args, **__: PARAMS.kwargs) -> RETURN | None:
            try:
                value = method(*_, **__)
                return value

            except Exception as err:
                action(err, *_, **__)
                raise err

        return wrapped_method

    return dec
