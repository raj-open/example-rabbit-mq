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
    "get_http_host_name_rabbit",
    "get_http_password_rabbit_admin",
    "get_http_password_rabbit_guest",
    "get_http_port_rabbit_queue",
    "get_http_port_rabbit_web",
    "get_http_user_rabbit_admin",
    "get_http_user_rabbit_guest",
]

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


@add_environment
def get_http_host_name_rabbit(
    # DEV-NOTE: from decorator
    path: str,
    env: dict[str, str],
    # end decorator args
) -> str:
    name = env["HTTP_HOST_NAME_RABBIT"]
    return name


@add_environment
def get_http_port_rabbit_web(
    # DEV-NOTE: from decorator
    path: str,
    env: dict[str, str],
    # end decorator args
) -> int:
    value = env["HTTP_PORT_RABBIT_WEB"]
    return int(value)


@add_environment
def get_http_port_rabbit_queue(
    # DEV-NOTE: from decorator
    path: str,
    env: dict[str, str],
    # end decorator args
) -> int:
    value = env["HTTP_PORT_RABBIT_QUEUE"]
    return int(value)


@add_environment
def get_http_user_rabbit_admin(
    # DEV-NOTE: from decorator
    path: str,
    env: dict[str, Any],
    # end decorator args
) -> str:
    """
    Gets http user.
    If value not set in .env, will raise a (Key)Exception.
    """
    value = env["HTTP_ADMIN_USER_RABBIT"]
    return value


@add_environment
def get_http_password_rabbit_admin(
    # DEV-NOTE: from decorator
    path: str,
    env: dict[str, Any],
    # end decorator args
) -> SecretStr:
    """
    Gets http password.
    If value not set in .env, will raise a (Key)Exception.
    """
    value = env["HTTP_ADMIN_PASSWORD_RABBIT"]
    return SecretStr(value)


@add_environment
def get_http_user_rabbit_guest(
    # DEV-NOTE: from decorator
    path: str,
    env: dict[str, Any],
    # end decorator args
) -> str:
    """
    Gets http user.
    If value not set in .env, will raise a (Key)Exception.
    """
    value = env["HTTP_GUEST_USER_RABBIT"]
    return value


@add_environment
def get_http_password_rabbit_guest(
    # DEV-NOTE: from decorator
    path: str,
    env: dict[str, Any],
    # end decorator args
) -> SecretStr:
    """
    Gets http password.
    If value not set in .env, will raise a (Key)Exception.
    """
    value = env["HTTP_GUEST_PASSWORD_RABBIT"]
    return SecretStr(value)
