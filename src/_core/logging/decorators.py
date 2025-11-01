#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from contextvars import ContextVar
from functools import wraps
from typing import Awaitable
from typing import Callable
from typing import Generator
from typing import ParamSpec
from typing import TypeVar

from safetywrap import Err

from ..utils.basic import *
from ..utils.time import *
from .constants import *
from .special import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "echo_async_function",
    "echo_function",
    "echo_generator",
]

# ----------------------------------------------------------------
# LOCAL CONSTANTS/VARIABLES
# ----------------------------------------------------------------

PARAMS = ParamSpec("PARAMS")
TX = TypeVar("TX")
RX = TypeVar("RX")
RETURN = TypeVar("RETURN")
_DEPTH = ContextVar("depth", default=[0])

# ----------------------------------------------------------------
# DECORATORS
# ----------------------------------------------------------------


def echo_function(
    *,
    tag: str | None = None,
    message: str | None = None,
    level: LOG_LEVELS | int | None = None,
    close: bool = True,
    depth: int | None = None,
):
    """
    Decorates a method via logging before and after (including in the case of errors).
    """

    def dec(
        action: Callable[PARAMS, RETURN],
        /,
    ) -> Callable[PARAMS, RETURN]:
        # prepare the message
        tag_ = tag or f"fct:{action.__name__}"
        message_ = message or tag_

        # modify function
        @wraps(action)
        def wrapped_action(*_: PARAMS.args, **__: PARAMS.kwargs) -> RETURN:
            timer = Timer(logger=None)
            message_end, message_error = echo_beginning(_, __, timer=timer, depth=depth, close=close, message=message_, level=level)  # fmt: skip

            try:
                output = action(*_, **__)
                match output:
                    case Err():
                        echo_end(timer=timer, close=close, message=message_error, level=level)  # fmt: skip
                        return output

                    # case Ok() | _:
                    case _:
                        echo_end(timer=timer, close=close, message=message_end, level=level)  # fmt: skip

                return output

            except BaseException as err:
                echo_end(timer=timer, close=close, message=message_error, level=level)  # fmt: skip
                raise err

        return wrapped_action

    return dec


def echo_generator(
    *,
    tag: str | None = None,
    message: str | None = None,
    level: LOG_LEVELS | int | None = None,
    close: bool = True,
    depth: int | None = None,
):
    """
    Decorates a method with Generator return type,
    via logging before and after (including in the case of errors).
    """

    def dec(
        action: Callable[PARAMS, Generator[TX, RX, RETURN]],
        /,
    ) -> Callable[PARAMS, Generator[TX, RX, RETURN]]:
        # prepare the message
        tag_ = tag or f"fct:{action.__name__}"
        message_ = message or tag_

        # modify function
        @wraps(action)
        def wrapped_action(*_: PARAMS.args, **__: PARAMS.kwargs) -> Generator[TX, RX, RETURN]:
            timer = Timer(logger=None)
            message_end, message_error = echo_beginning(_, __, timer=timer, depth=depth, close=close, message=message_, level=level)  # fmt: skip

            try:
                output = yield from action(*_, **__)
                match output:
                    case Err():
                        echo_end(timer=timer, close=close, message=message_error, level=level)  # fmt: skip

                    # case Ok() | _:
                    case _:
                        echo_end(timer=timer, close=close, message=message_end, level=level)  # fmt: skip

                return output

            except BaseException as err:
                echo_end(timer=timer, close=close, message=message_error, level=level)  # fmt: skip
                raise err

        return wrapped_action

    return dec


def echo_async_function(
    *,
    tag: str | None = None,
    message: str | None = None,
    level: LOG_LEVELS | int | None = None,
    close: bool = True,
    depth: int | None = None,
):
    """
    Decorates an async method via logging before and after (including in the case of errors).
    """

    def dec(
        action: Callable[PARAMS, Awaitable[RETURN]],
        /,
    ) -> Callable[PARAMS, Awaitable[RETURN]]:
        # prepare the message
        tag_ = tag or f"fct:{action.__name__}"
        message_ = message or tag_

        # modify function
        @wraps(action)
        async def wrapped_action(*_: PARAMS.args, **__: PARAMS.kwargs) -> RETURN:
            timer = Timer(logger=None)
            message_end, message_error = echo_beginning(_, __, timer=timer, depth=depth, close=close, message=message_, level=level)  # fmt: skip

            try:
                output = await action(*_, **__)
                echo_end(timer=timer, close=close, message=message_end, level=level)  # fmt: skip
                return output

            except BaseException as err:
                echo_end(timer=timer, close=close, message=message_error, level=level)  # fmt: skip
                raise err

        return wrapped_action

    return dec


# ----------------------------------------------------------------
# AUXILIARY METHODS
# ----------------------------------------------------------------


def echo_beginning(
    posargs: tuple,
    kwargs: dict,
    /,
    *,
    timer: Timer,
    depth: int | None,
    close: bool,
    message: str,
    level: LOG_LEVELS | int | None,
) -> tuple[str, str]:
    """
    Auxiliary method to be performed at the start of an echo-decorated method.
    """
    depths = _DEPTH.get() or [0]
    depth = depth or depths[-1]  # either pick latest value or forced value

    message__ = safe_format_string(message, *posargs, **kwargs)

    message_start = "=" * (depth + 1) + "> [ ] " + message__
    message_end = message_error = ""
    if close:
        message_end = "=" * (depth + 1) + "> [/] " + message__ + " | elapsed: {t:.2f}s"  # fmt: skip
        message_error = "=" * (depth + 1) + "> [x] " + message__ + " | elapsed: {t:.2f}s"  # fmt: skip

    log(message_start, level=level)
    _DEPTH.set([*depths, depth + 1])
    timer.start()

    return message_end, message_error


def echo_end(
    *,
    timer: Timer,
    close: bool,
    message: str,
    level: LOG_LEVELS | int | None,
) -> tuple[str, str]:
    """
    Auxiliary method to be performed at the end of an echo-decorated method.
    """
    depths = _DEPTH.get()
    _DEPTH.set(depths[:-1] or [0])  # remove last value
    if close:
        msg = safe_format_string(message, t=timer.elapsed)
        log(msg, level=level)
