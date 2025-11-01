#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API endpoints basic.
"""

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from typing import Annotated

from fastapi import Depends
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter
from fastapi.security import HTTPBasic
from fastapi.security import HTTPBasicCredentials
from fastapi.templating import Jinja2Templates

from ..endpoints import endpoints_basic as ep
from .decorators import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "add_endpoints_basic",
]

# ----------------------------------------------------------------
# ENDPOINTS
# ----------------------------------------------------------------


def add_endpoints_basic(
    app: FastAPI | APIRouter,
    /,
    *,
    tag: str,
    route: str,
    sec: HTTPBasic,
    tmplt: Jinja2Templates,
):
    """
    Adds basic endpoints.
    """

    @app.get("/", summary="", tags=[], include_in_schema=False)
    async def method():
        return RedirectResponse(f"{route}/docs")

    @app.get(
        "/ping",
        summary="Ping api",
        tags=[tag],
        include_in_schema=True,
    )
    @catch_internal_server_error
    @output_as_bytes
    async def method():
        """
        An endpoint for debugging.
        """
        return "success"

    @app.get(
        "/version",
        summary="Display the VERSION of the programme",
        tags=[tag],
        include_in_schema=True,
    )
    @catch_internal_server_error
    @add_http_auth
    async def method(
        # DEV-NOTE: add for @add_http_auth-decorator
        http_cred: Annotated[HTTPBasicCredentials, Depends(sec)],
        # end of decorator arguments
        /,
    ):
        version = ep.endpoint_version()
        return version
