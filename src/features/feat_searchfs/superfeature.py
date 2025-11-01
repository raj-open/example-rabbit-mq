#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import logging

from safetywrap import Err
from safetywrap import Ok
from safetywrap import Result

from ..._core.utils.code import *
from ...models.application import *
from .feature import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "superfeature",
]

# ----------------------------------------------------------------
# WRAPPED FEATURES
# ----------------------------------------------------------------


def superfeature(
    tasks: list[RequestTask],
    /,
) -> Result[str, list[str]]:
    """
    Calls `SEARCH-FS` features for a list of tasks
    """
    errors = list[str]()
    n_tot = len(tasks)
    for task in tasks:
        result = feature(
            label=task.label,
            ref_inputs=task.data.inputs,
            options=task.options,
        )

        if isinstance(result, Err):
            errors.append(result.unwrap_err())

    if (n := len(errors)) > 0:
        match n, n_tot:
            case 1, 1:
                # NOTE: logging superfluous
                pass

            case _, _ if n == n_tot:
                logging.warning(f"all of the {n_tot} tasks failed")

            case _:
                logging.warning(f"{n} of the {n_tot} tasks failed")

        return Err(errors)

    return Ok("success")
