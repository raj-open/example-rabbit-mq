#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from typing import Any

from pydantic import SecretStr

from .basic import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "get_http_ip",
    "get_http_password",
    "get_http_port",
    "get_http_user",
]

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


@add_environment
def get_http_route(
    # DEV-NOTE: from decorator
    path: str,
    env: dict[str, str],
    # end decorator args
    default: str = "",
) -> str:
    route = env.get("HTTP_ROUTE", default)
    # ensure route starts with "/"
    route = route.lstrip(" /")
    route = f"/{route}"
    # NOTE: in particular route = "/" is avoided
    route = route.rstrip(" /")
    return route


@add_environment
def get_http_ip(
    # DEV-NOTE: from decorator
    path: str,
    env: dict[str, str],
    # end decorator args
) -> str:
    return env["HTTP_IP"]


@add_environment
def get_http_port(
    # DEV-NOTE: from decorator
    path: str,
    env: dict[str, str],
    # end decorator args
) -> int:
    value = env["HTTP_PORT"]
    return int(value)


@add_environment
def get_http_user(
    # DEV-NOTE: from decorator
    path: str,
    env: dict[str, Any],
    # end decorator args
    default: str = "admin",
) -> str:
    """
    Gets http user.
    If value not set in .env, will raise a (Key)Exception.
    """
    value = env["HTTP_USER"]
    return value


@add_environment
def get_http_password(
    # DEV-NOTE: from decorator
    path: str,
    env: dict[str, Any],
    # end decorator args
) -> SecretStr:
    """
    Gets http password.
    If value not set in .env, will raise a (Key)Exception.
    """
    value = env["HTTP_PASSWORD"]
    return SecretStr(value)
