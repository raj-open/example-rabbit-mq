#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import logging
from datetime import datetime

from safetywrap import Err
from safetywrap import Ok
from safetywrap import Result

from ..._core.logging import *
from ...algorithms.filesmanager import *
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
    # NOTE: currently unused
    # cfg_general = config.parser_config().parse()
    managers = config.get_managers()

    try:
        # locate directory in file system
        root = ref_inputs.path
        loc = ref_inputs.location
        manager = managers[loc]

        # determine computational limits
        max_depth = options.max_depth
        max_items = options.max_items
        dt = options.max_duration
        t = datetime.now()
        t_max = t + dt

        # run search algorithm and apply guards to prevent unlimited search duration
        count = 0
        for d, subpath, filename in recursive_file_search(manager, path=root):
            # terminate if search takes too long
            if (t := datetime.now()) >= t_max:
                raise TimeoutError(f"search algorithm terminated - exceeded maximum tolerated duration of {dt}")  # fmt: skip

            # terminate if depth exceeds limits
            if d > max_depth:
                raise Exception(f"search algorithm terminated - directory depth exceeeded maximum tolerated depth of {max_depth}")  # fmt: skip

            # terminate if number of items exceeds limits
            count += 1
            if count > max_items:
                raise Exception(f"search algorithm terminated - item count exceeededs maximum tolerated value of {max_items}")  # fmt: skip

            logging.warning(f"notify '{subpath}/{filename}' - not yet implemented")

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
