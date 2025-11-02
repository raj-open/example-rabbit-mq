#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import logging

from safetywrap import Err
from safetywrap import Ok
from safetywrap import Result

from ..._core.utils.time import *
from ...models.apis.queue import *
from ...models.application import *
from ...models.datasources import *
from ...models.internal.errors import *
from ...setup import *
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
    feat = EnumFeatures.SEARCH_FS
    # NOTE: currently unused
    # cfg_general = config.parser_config().parse()
    errors = list[JSON_TYPE]()
    msg_exchange = ""
    n_tot = len(tasks)
    settings = config.get_queue_parameters()

    """
    Establish connection to message queue
    """

    with ChannelContext(settings) as chan:
        # FIXME: publication to exchages fails when msg_exchange is not ""
        # chan.exchange_declare(exchange=msg_exchange, exchange_type="direct")

        # perform each task an log each case to different route
        for task in tasks:
            msg_route = f"[{feat.value}].[{task.label}]"

            # ensure case has its own route and that it is cleared
            chan.queue_declare(queue=msg_route)
            if task.options.reset_queue:
                chan.queue_purge(queue=msg_route)

            """
            Run feature with error handling
            """

            try:
                feature(
                    chan,
                    label=task.label,
                    ref=task.data.inputs,
                    options=task.options,
                    msg_exchange=msg_exchange,
                    msg_route=msg_route,
                )

            except ExceptionWithData as err:
                msg = str(err)
                logging.error(msg)
                err.add_data("label", task.label)
                body = {
                    "timestamp": get_datetime_stamp(),
                    "message": str(err),
                    "code": err.code or 500,
                    "data": err.data,
                }
                errors.append(body)
                contents = serialise_any_element(body)
                chan.basic_publish(exchange=msg_exchange, routing_key=msg_route, body=contents, properties=RABBIG_LOG_LEVEL_ERROR)  # fmt: skip

            except Exception as err:
                msg = str(err)
                logging.error(msg)
                body = {
                    "timestamp": get_datetime_stamp(),
                    "message": msg,
                    "data": {
                        "label": task.label,
                    },
                }
                errors.append(body)
                contents = serialise_any_element(body)
                chan.basic_publish(exchange=msg_exchange, routing_key=msg_route, body=contents, properties=RABBIG_LOG_LEVEL_ERROR)  # fmt: skip

            except BaseException as err:
                # DEV-NOTE: pass on all other kinds of exceptions
                msg = f"task terminated - {err}"
                body = {
                    "timestamp": get_datetime_stamp(),
                    "message": msg,
                    "data": {
                        "label": task.label,
                    },
                }
                errors.append(body)
                contents = serialise_any_element(body)
                chan.basic_publish(exchange=msg_exchange, routing_key=msg_route, body=contents, properties=RABBIG_LOG_LEVEL_ERROR)  # fmt: skip
                raise err

    """
    Finally error handling
    """

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

    """
    No errors - all tasks successful
    """

    return Ok("success")
