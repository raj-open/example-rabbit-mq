#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This submodule provides the generic FilesManager interface
"""

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from ..generated.application import EnumDataFileFormat
from ..generated.application import EnumFilesSystem
from ..generated.application import FileRef
from ..generated.application import MetaData
from ..generated.application import ProxyConfig
from .config import *
from .os import *
from .payloads import *
from .traits import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "ConfigLoader",
    "EnumDataFileFormat",
    "EnumFilesSystem",
    "FileRef",
    "FilesManager",
    "FilesManagerFile",
    "FilesManagerFolder",
    "MetaData",
    "OSFilesManager",
    "OSFilesManagerFile",
    "OSFilesManagerFolder",
    "PayloadParser",
    "ProxyConfig",
]
