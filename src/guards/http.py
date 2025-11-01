#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from fastapi.security import HTTPBasicCredentials

from ..setup import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "guard_http_credentials",
    "guard_http_password",
    "guard_http_user",
]

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def guard_http_user(value: str, /):
    """
    A guard which checks if http username is valid.
    """
    value_expected = config.http_user()
    if value != value_expected:
        raise ValueError("Invalid http username")


def guard_http_password(value: str, /):
    """
    A guard which checks if http password is valid.
    """
    value_expected = config.http_password().get_secret_value()
    if value != value_expected:
        raise ValueError("Invalid http password!")


def guard_http_credentials(
    cred: HTTPBasicCredentials,
    /,
):
    """
    A guard which checks if http credentials are valid.
    """
    try:
        guard_http_user(cred.username)
        guard_http_password(cred.password)

    except Exception as err:
        # msg = str(err)
        msg = "Invalid http credentials!"
        raise ValueError(msg)
