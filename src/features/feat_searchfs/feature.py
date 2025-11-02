#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import json
import logging
from datetime import datetime
from datetime import timedelta
from functools import partial

from pika import BasicProperties
from safetywrap import Err
from safetywrap import Ok
from safetywrap import Result

from ..._core.logging import *
from ...algorithms.filesmanager import *
from ...models.apis.queue import *
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
    ref: FileRef,
    options: RequestTaskOptions,
) -> Result[str, str]:
    """
    Feature `SEARCH-FS`
    """
    feat = EnumFeatures.SEARCH_FS
    # NOTE: currently unused
    # cfg_general = config.parser_config().parse()
    managers = config.get_managers()

    # create guard to safeguard against computational limits
    guard = partial(
        guard_limits,
        max_depth=options.max_depth,
        max_items=options.max_items,
        max_duration=options.max_duration,
        t_max=datetime.now() + options.max_duration,
    )

    try:
        """
        connect to message queue and perform task
        """
        # FIXME: publication to exchages fails
        # msg_exchange = feat.value
        msg_exchange = ""
        msg_route = label
        msg_properties = BasicProperties(type="info")

        settings = config.get_queue_parameters()
        with ChannelContext(settings=settings) as chan:
            # FIXME: publication to exchages fails
            # chan.exchange_declare(exchange=msg_exchange, exchange_type="direct")
            chan.queue_declare(queue=msg_route)

            # locate directory in file system
            root = ref.path
            loc = ref.location
            manager = managers[loc]

            """
            run search algorithm and apply guards to prevent unlimited search duration
            """
            for count, (d, subpath, filename) in enumerate(
                # NOTE: algorithm returns a generator
                recursive_file_search(
                    manager,
                    path=root,
                    skip_empty=options.skip_empty,
                ),
                # keep track of number of items found
                start=1,
            ):
                # apply guard
                guard(d=d, count=count)

                # if not blocked by guard log to queue
                body = {"path": subpath, "filename": filename}
                contents = json.dumps(body).encode()
                chan.basic_publish(
                    exchange=msg_exchange,
                    routing_key=msg_route,
                    body=contents,
                    properties=msg_properties,
                )

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


# ----------------------------------------------------------------
# AUXILIARY METHODS
# ----------------------------------------------------------------


def guard_limits(
    *,
    d: int,
    count: int,
    max_depth: int,
    max_items: int,
    max_duration: timedelta,
    t_max: datetime,
):
    """
    Applies guard clauses to terminate search algorithm if limits are breached
    """
    # terminate if search takes too long
    if datetime.now() >= t_max:
        raise TimeoutError(f"search algorithm terminated - exceeded maximum tolerated duration of {max_duration}")  # fmt: skip

    # terminate if depth exceeds limits
    if d > max_depth:
        raise Exception(f"search algorithm terminated - directory depth exceeeded maximum tolerated depth of {max_depth}")  # fmt: skip

    # terminate if number of items exceeds limits
    if count > max_items:
        raise Exception(f"search algorithm terminated - item count exceeededs maximum tolerated value of {max_items}")  # fmt: skip
