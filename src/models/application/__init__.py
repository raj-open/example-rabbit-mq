#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from ..generated.application import EnumFeatures
from ..generated.application import GeneralConfig
from ..generated.application import RepoInfo
from ..generated.application import RequestTask
from ..generated.application import RequestTaskData
from ..generated.application import RequestTaskOptions
from ..generated.application import RequestsPayload

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "EnumFeatures",
    "GeneralConfig",
    "RepoInfo",
    "RequestTask",
    "RequestTaskData",
    "RequestTaskOptions",
    "RequestsPayload",
    "parse_tasks",
]


# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def parse_tasks(payload: RequestsPayload, /) -> list[RequestTask]:
    """
    Given a payload retuns the list of tasks it encodes
    """
    match payload.root:
        case list() as tasks:
            return tasks

        case _ as task:
            return [task]
