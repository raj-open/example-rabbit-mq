#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import os
from functools import wraps
from typing import Callable
from typing import Concatenate
from typing import ParamSpec
from typing import TypeVar

from dotenv import dotenv_values
from dotenv import load_dotenv

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "add_environment",
    "get_environment",
]

# ----------------------------------------------------------------
# LOCAL CONSTANTS/VARIABLES
# ----------------------------------------------------------------

PARAMS = ParamSpec("PARAMS")
RETURN = TypeVar("RETURN")

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def get_environment(path: str, /) -> dict[str, str]:
    """
    Loads environment variables from

    - bash session
    - a given .env file

    Values in session are ignored if empty-like.

    If a key is in both the session and file,
    then the session-value takes precedence,
    allowing users to change environments on-the-fly.
    """
    # values in file
    environ_file = dotenv_values(path)

    # load from session
    load_dotenv(dotenv_path=path)
    env_from_session = {
        key: value
        for key, value in os.environ.items()
        # NOTE: filter out empty/null values
        if value not in [None, ""]
    }

    # load from file
    env_from_file = {
        key: value
        for key, value in environ_file.items()
        # NOTE: allow file to include empty/null values
        # if value not in [None, ""]
    }

    # session env vars take precedence
    # NOTE: left-right = low to higher precedence
    env = env_from_file | env_from_session

    return dict(env)


def add_environment(
    action: Callable[
        Concatenate[str, dict[str, str], PARAMS],
        RETURN,
    ],
    /,
) -> Callable[Concatenate[str, PARAMS], RETURN]:
    """
    Decorates method to make it get environment first.
    Runs method with error wrapping,
    catching errors with a ValueError
    """

    # modify function
    @wraps(action)
    def wrapped_action(path: str, *_: PARAMS.args, **__: PARAMS.kwargs) -> RETURN:
        env = get_environment(path)
        result = action(path, env, *_, **__)
        return result

    return wrapped_action
