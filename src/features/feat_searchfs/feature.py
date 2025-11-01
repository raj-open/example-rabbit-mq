#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import logging

from safetywrap import Err
from safetywrap import Ok
from safetywrap import Result

from ..._core.logging import *
from ...models.application import *
from ...models.filesmanager import *
from ...models.internal.errors import *
from ...setup import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "feature",
]

# ----------------------------------------------------------------
# FEATURE
# ----------------------------------------------------------------


@echo_function(
    tag="FEATURE - SEARCH-FS | '{label}'",
    level="INFO",
    depth=0,
)
def feature(
    *,
    label: str,
    ref_inputs: FileRef,
    options: RequestTaskOptions,
) -> Result[str, str]:
    """
    Feature `SEARCH-FS`
    """
    try:
        managers = config.get_managers()
        cfg_general = config.parser_config().parse()

        raise NotImplementedError("feature SEARCH-FS not yet implemented")

        return Ok("success")

    except ExceptionWithData as err:
        msg = f"task '{label}' failed with error code {err.code or 500} - {err}"  # fmt: skip
        logging.error(msg)
        return Err(msg)

    except Exception as err:
        msg = f"task '{label}' failed - {err}"  # fmt: skip
        logging.error(msg)
        return Err(msg)

    except BaseException as err:
        # DEV-NOTE: pass on all other kinds of exceptions
        raise err
