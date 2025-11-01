#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main script to creates the FastAPI instance,
including resources and endpoints.
"""

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.security import HTTPBasic
from fastapi.templating import Jinja2Templates
from fastapi_offline import FastAPIOffline

from ...setup import *
from .endpoints_basic import *
from .endpoints_features import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "create_ui",
]

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def create_ui(
    *,
    route: str = "",
    debug: bool = False,
) -> FastAPI:
    """
    Creates the API and adds endpoints

    **NOTE:** Uses `fastapi-offline` so that can be run offline.
    """
    app = FastAPIOffline(
        docs_url=f"{route}/docs",
        title=config.INFO.name.title(),
        description=config.INFO.description,
        version=config.INFO.version,
        debug=debug,
        # see https://fastapi.tiangolo.com/how-to/configure-swagger-ui
        # and https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration
        swagger_ui_parameters={
            "docExpansion": "list",
            "defaultModelsExpandDepth": 0,
            "displayRequestDuration": True,
            "syntaxHighlight": True,
            "syntaxHighlight.theme": "obsidian",
        },
    )
    router = APIRouter()
    # add_resources(router, route=route)
    add_endpoints(router, route=route)
    app.include_router(router, prefix=route)
    return app


# def add_resources(
#     app: FastAPI | APIRouter,
#     /,
#     *,
#     route: str,
# ):
#     """
#     Connects static resources.
#     """
#     app.mount(f"{route}/index.html", StaticFiles(directory="src/app/static", html=True), name="nodejs")
#     return


def add_endpoints(
    app: FastAPI | APIRouter,
    /,
    *,
    route: str,
):
    """
    Sets all the endpoints for the API.
    """
    sec_http = HTTPBasic()
    tmplt = Jinja2Templates(directory="src/app/static")

    add_endpoints_basic(app, tag="Basic", route=route, sec=sec_http, tmplt=tmplt)
    add_endpoints_features(app, tag="Features", route=route, sec=sec_http, tmplt=tmplt)
    return
