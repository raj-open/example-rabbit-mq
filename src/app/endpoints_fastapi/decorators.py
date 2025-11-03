#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import logging
from functools import wraps
from typing import Any
from typing import Awaitable
from typing import Callable
from typing import Concatenate
from typing import ParamSpec
from typing import TypeVar

from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel
from safetywrap import Err
from safetywrap import Ok

from ..._core.constants import *
from ..._core.logging import *
from ..._core.utils.any import *
from ..._core.utils.serialise import *
from ...guards.http import *
from ...models.filesmanager import *
from ...models.internal import *
from ...setup import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "add_http_auth",
    "catch_internal_server_error",
    "output_as_bytes",
    "parse_payload",
]

# ----------------------------------------------------------------
# LOCAL CONSTANTS/VARIABLES
# ----------------------------------------------------------------

PARAMS = ParamSpec("PARAMS")
T1 = TypeVar("T1")
T2 = TypeVar("T2")
MODEL = TypeVar("MODEL")
RETURN = TypeVar("RETURN")
CODE_DEFAULT = 500

# ----------------------------------------------------------------
# DECORATORS
# ----------------------------------------------------------------


def catch_internal_server_error(
    action: Callable[PARAMS, Awaitable[RETURN]],
    /,
):
    """
    Decorates and endpoint by returning internal server error if error occurs.
    """

    # modify function
    @wraps(action)
    async def wrapped_action(
        *_: PARAMS.args,
        **__: PARAMS.kwargs,
    ) -> RETURN:
        try:
            output = await action(*_, **__)
            return output

        except TypeError as err:
            logging.error(err)
            code = 422
            err_str = str(err)

        except ExceptionWithData as err:
            logging.error(err)
            err_str = str(err)
            code = err.code or CODE_DEFAULT

        except Exception as err:
            logging.error(err)
            err_str = error_with_trace(err)
            err_str = str(err)
            code = 500

        except BaseException as err:
            logging.error(err)
            err_str = str(err)
            code = 500

        # NOTE: headers MUST be string-valued!
        headers = dict(
            code=str(code),
            message=err_str,
        )
        raise HTTPException(status_code=code, detail=err_str, headers=headers)

    return wrapped_action


def output_as_bytes(
    action: Callable[
        PARAMS,
        Awaitable[Any],
    ],
    /,
):
    """
    Decorates endpoint with parsed query params and deserialised body
    """

    @wraps(action)
    async def wrapped_action(
        *_: PARAMS.args,
        **__: PARAMS.kwargs,
    ) -> JSONResponse:
        # run method
        result = await action(*_, **__)

        # unwrap safety
        code = 200
        match result:
            case Err() as err:
                code = 500
                result = err.unwrap_err()

            case Ok():
                result = result.unwrap()

        # serialise result
        contents = serialise_any_as_object(result).unwrap_or(None)  # fmt: skip

        # prepare response
        response = JSONResponse(contents, status_code=code)

        return response

    return wrapped_action


def add_http_auth(
    action: Callable[
        Concatenate[HTTPBasicCredentials, PARAMS],
        Awaitable[RETURN],
    ],
    /,
):
    """
    Decorates and endpoint by adding basic http-authorisation to it.

    **DEV-NOTE:**
    Signature cannot change when using `FastAPI`'s
    `@app.get`, `@app.post`, etc. decorators.
    Thus need to include all arguments needed by our decorators,
    even if superfluous inside undecorated part.
    """

    # modify function - but with different signature!
    @wraps(action)
    async def wrapped_action(
        http_cred: HTTPBasicCredentials,
        *_: PARAMS.args,
        **__: PARAMS.kwargs,
    ) -> RETURN:
        try:
            guard_http_credentials(http_cred)

        except Exception as err:
            logging.error(err)
            raise HTTPException(status_code=401, detail=err)

        output = await action(http_cred, *_, **__)
        return output

    return wrapped_action


def parse_payload(
    type_: type[BaseModel],
    /,
):
    """
    Parsers arbitrary payloads
    """

    async def method(
        request: Request,
        /,
    ) -> MODEL:
        try:
            content_type = request.headers.get("Content-Type")
            fmt = MAP_MIME_TYPE_TO_FILETYPE.get(content_type)
            contents = await request.body()

            parser = PayloadParser[MODEL](type_=type_, managers=config.get_managers())
            payload = parser.parse(contents, format=fmt)
            return payload

        except Exception as err:
            raise TypeError(f"could not parse payload in body - {err}")

    return method
