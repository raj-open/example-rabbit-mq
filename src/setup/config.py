#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import logging
from contextvars import ContextVar
from pathlib import Path

import toml
from pika import ConnectionParameters
from pika import PlainCredentials
from pydantic import SecretStr

from ..__paths__ import *
from .._core.constants import *
from .._core.logging import *
from .._core.utils.code import *
from .._core.utils.time import *
from ..models.application import *
from ..models.filesmanager import *
from ..models.internal import *
from ..queries.environment import *
from ..queries.filesmanager import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "INFO",
    "TIMEZONE",
    "VERSION",
]

# ----------------------------------------------------------------
# GLOBAL PROPERTIES
# ----------------------------------------------------------------

pid = ContextVar[int]("pid")  # fmt: skip
path_env = ContextVar[str]("path env", default=".env")  # fmt: skip
path_logging = Property[str | None](label="path logging", factory=lambda: get_path_logs(path_env.get()))  # fmt: skip
path_config = Property[str](label="path application config", factory=lambda: get_root_path("setup", "config.yaml"))  # fmt: skip
path_requests = Property[str](label="path user requests", factory=lambda: get_root_path("setup", "requests.yaml"))  # fmt: skip

# for api server
http_ip = Property[str](label="http ip", factory=lambda: get_http_ip(path_env.get()))  # fmt: skip
http_port = Property[int](label="http port", factory=lambda: get_http_port(path_env.get()))  # fmt: skip
http_user = Property[str](label="http user", factory=lambda: get_http_user(path_env.get()))  # fmt: skip
http_password = Property[SecretStr](label="http password", factory=lambda: get_http_password(path_env.get()))  # fmt: skip
shared_network = Property[bool](label="is in docker network", factory=lambda: get_shared_network(path_env.get()))  # fmt: skip

# for rabbit/queue
http_host_name_rabbit = Property[str](label="host name of rabbit mq", factory=lambda: get_http_host_name_rabbit(path_env.get()))  # fmt: skip
http_port_rabbit_queue = Property[int](label="port of rabbit queue", factory=lambda: get_http_port_rabbit_queue(path_env.get()))  # fmt: skip
http_port_rabbit_web = Property[int](label="port of rabbit admin", factory=lambda: get_http_port_rabbit_web(path_env.get()))  # fmt: skip
http_user_rabbit_admin = Property[str](label="admin username for rabbit mq", factory=lambda: get_http_user_rabbit_admin(path_env.get()))  # fmt: skip
http_password_rabbit_admin = Property[SecretStr](label="admin password for rabbit mq", factory=lambda: get_http_password_rabbit_admin(path_env.get()))  # fmt: skip
http_user_rabbit_guest = Property[str](label="guest username for rabbit mq", factory=lambda: get_http_user_rabbit_guest(path_env.get()))  # fmt: skip
http_password_rabbit_guest = Property[SecretStr](label="guest password for rabbit mq", factory=lambda: get_http_password_rabbit_guest(path_env.get()))  # fmt: skip

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def initialise_application(
    *,
    name: str,
    title: str | None = None,
    verbose: bool = False,
    serialise: bool = True,
    log_to_files: bool = False,
):
    """
    Initialises logging and displays information about pid, cpus.
    """
    level = "DEBUG" if verbose else "INFO"
    path = path_logging.get() if log_to_files else None
    configure_logging(name="root", level=level, path=path, serialise=serialise)  # fmt: skip

    logging.info(f"running {title or name} v{INFO.version} on PID {pid.get()}")
    return


# ----------------------------------------------------------------
# QUERIES
# ----------------------------------------------------------------


@compute_once
def load_repo_info() -> RepoInfo:
    path = Path(get_root_path(), "pyproject.toml").as_posix()
    with open(path, "r") as fp:
        config_repo = toml.load(fp)
        assets = config_repo.get("project", {})
        info = RepoInfo.model_validate(assets)
        return info


@compute_once
def get_version() -> str:
    info = load_repo_info()
    return info.version


@compute_once
def get_managers() -> dict[EnumFilesSystem, FilesManager]:
    """
    Returns managers to access files in different locations.
    """
    return {
        EnumFilesSystem.OS: get_files_manager(EnumFilesSystem.OS, tz=TIMEZONE),
        # TODO: implement use of credentials and add protocols for other file systems
        # EnumFilesSystem.SHAREPOINT: get_files_manager(EnumFilesSystem.SHAREPOINT, tz=TIMEZONE),
        # EnumFilesSystem.BLOB_STORAGE: get_files_manager(EnumFilesSystem.BLOB_STORAGE, tz=TIMEZONE),
    }


@compute_once
def get_queue_parameters() -> ConnectionParameters:
    """
    Returns connection parameters for queue
    """
    # use guest credentials
    user = http_user_rabbit_guest()
    pw = http_password_rabbit_guest().get_secret_value()
    creds = PlainCredentials(username=user, password=pw)

    # NOTE: valid value of host depends on whether application is shared network
    host = http_ip()
    if shared_network():
        host = http_host_name_rabbit()
    port = http_port_rabbit_queue()

    # apply to queue
    settings = ConnectionParameters(host=host, port=port, credentials=creds)  # fmt: skip
    return settings


# ----------------------------------------------------------------
# LAZY LOADED RESOURCES / PROPERTIES
# ----------------------------------------------------------------

INFO = load_repo_info()
VERSION = get_version()
TIMEZONE = get_local_timezone()

parser_requests = Property[PayloadParser[RequestsPayload]](
    label="parser:requests payload",
    factory=lambda: PayloadParser(type_=RequestsPayload, managers=get_managers(), location="OS", root=path_requests.get()),
)  # fmt: skip

parser_config = Property[PayloadParser[GeneralConfig]](
    label="parser:general application config",
    factory=lambda: PayloadParser(type_=GeneralConfig, managers=get_managers(), location="OS", root=path_config.get()),
)  # fmt: skip
