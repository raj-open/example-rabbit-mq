#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API endpoints for main features.
"""

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from typing import Annotated

from fastapi import Depends
from fastapi import FastAPI
from fastapi import Request
from fastapi.routing import APIRouter
from fastapi.security import HTTPBasic
from fastapi.security import HTTPBasicCredentials
from fastapi.templating import Jinja2Templates

from ...features import *
from ...models.application import *
from .decorators import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "add_endpoints_features",
]

# ----------------------------------------------------------------
# ENDPOINTS
# ----------------------------------------------------------------


def add_endpoints_features(
    app: FastAPI | APIRouter,
    /,
    *,
    tag: str,
    route: str,
    sec: HTTPBasic,
    tmplt: Jinja2Templates,
):
    """
    Adds endpoints pertaining to the features of the repo.
    """

    @app.post(
        "/feature/search-fs",
        summary="Runs the feature SEARCH-FS",
        tags=[tag],
        include_in_schema=True,
    )
    @catch_internal_server_error
    @add_http_auth
    @output_as_bytes
    async def method(
        # DEV-NOTE: add for @add_http_auth-decorator
        http_cred: Annotated[HTTPBasicCredentials, Depends(sec)],
        # end of decorator arguments
        /,
        *,
        request: Request,
    ):
        # process body
        parser = parse_payload(RequestsPayload)
        contents: RequestsPayload = await parser(request)
        tasks = parse_tasks(contents)
        # perform feature
        result = feat_searchfs.superfeature(tasks)
        return result
