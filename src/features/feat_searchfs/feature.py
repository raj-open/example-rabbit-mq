#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from datetime import datetime
from datetime import timedelta
from functools import partial

from pika.adapters.blocking_connection import BlockingChannel

from ..._core.logging import *
from ..._core.utils.serialise import *
from ..._core.utils.time import *
from ...algorithms.filesmanager import *
from ...models.apis.queue import *
from ...models.application import *
from ...models.filesmanager import *
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
    chan: BlockingChannel,
    /,
    *,
    label: str,
    ref: FileRef,
    options: RequestTaskOptions,
    msg_exchange: str,
    msg_route: str,
):
    """
    Feature `SEARCH-FS`
    """
    # NOTE: currently unused
    # cfg_general = config.parser_config().parse()
    managers = config.get_managers()

    # locate directory in file system
    root = ref.path
    loc = ref.location
    manager = managers[loc]

    # create guard to safeguard against computational limits
    guard = partial(
        guard_limits,
        max_depth=options.max_depth,
        max_items=options.max_items,
        max_duration=options.max_duration,
        t_max=datetime.now() + options.max_duration,
    )

    # run search algorithm and apply guards to prevent unlimited search duration
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
        body = {
            "timestamp": get_datetime_stamp(),
            "path": subpath,
            "filename": filename,
        }
        contents = serialise_any_as_text(body).unwrap_or("")
        chan.basic_publish(
            exchange=msg_exchange,
            routing_key=msg_route,
            body=contents,
            properties=RABBIT_LOG_LEVEL_INFO,
        )

    return


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
    if datetime.now() > t_max:
        raise TimeoutError(f"search algorithm terminated - exceeded maximum tolerated duration of {max_duration}")  # fmt: skip

    # terminate if depth exceeds limits
    if d > max_depth:
        raise Exception(f"search algorithm terminated - directory depth exceeeded maximum tolerated depth of {max_depth}")  # fmt: skip

    # terminate if number of items exceeds limits
    if count > max_items:
        raise Exception(f"search algorithm terminated - item count exceeeded maximum tolerated value of {max_items}")  # fmt: skip
