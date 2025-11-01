#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import logging
from typing import Generic
from typing import TypeVar

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import SkipValidation

from ..._core.utils.io import *
from ..generated.application import EnumDataFileFormat
from ..generated.application import EnumFilesSystem
from ..generated.application import ProxyConfig
from .traits import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "ConfigLoader",
]

# ----------------------------------------------------------------
# CONSTANTS
# ----------------------------------------------------------------

T = TypeVar("T")

# ----------------------------------------------------------------
# CLASSES
# ----------------------------------------------------------------


class ConfigLoader(BaseModel, Generic[T]):
    """
    A generic class which provides a recursive method to load configs.

    ## Example load form file ##
    ```py
    loc = "..." # one off "OS", "SHAREPOINT", ...
    path = "..." # path in location
    managers = {
        "OS": ...,
        "SHAREPOINT": ...,
    }
    loader = ConfigLoader[GeneralConfig](managers=managers, type_=GeneralConfig)
    cfg = loader.load_from_file(loc=loc, path=path) # will be type GeneralConfig
    ```

    ## Example load form file ##
    ```py
    contents = b"..." # contents of file as bytes
    managers = {
        "OS": ...,
        "SHAREPOINT": ...,
    }
    loader = ConfigLoader[GeneralConfig](managers=managers, type_=GeneralConfig)
    cfg = loader.load_from_contents(contents) # will be type GeneralConfig
    ```
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    managers: dict[EnumFilesSystem, SkipValidation[FilesManager]]
    type_: type[BaseModel]

    def get_file_contents(
        self,
        /,
        *,
        loc: EnumFilesSystem,
        path: str,
    ) -> tuple[bytes, EnumDataFileFormat]:
        """
        Given a reference gets the file contents and file format.

        The absolute path is determined as follows:
        """
        # determine path
        manager = self.managers[loc]

        # get file extension -> format of file
        _, _, ext = manager.__class__.path_split(path)

        # get file and contents
        try:
            file = manager.get_file(path)
            contents = file.read_as_bytes()

        except Exception as err:
            logging.error(f"could not load or read {loc}-file in '{path}' - {err}")
            raise err

        try:
            fmt = EnumDataFileFormat(ext)

        except Exception as err:
            logging.error(f"unrecognised format {ext} - {err}")
            raise err

        return contents, fmt

    def load_from_file(
        self,
        /,
        *,
        loc: EnumFilesSystem,
        path: str,
        fmt: EnumDataFileFormat | None = None,
        chain: list[tuple[EnumFilesSystem, str]] | None = None,
    ) -> T:
        """
        Extracts config from file.

        NOTE: if `ref` attribute is set, will recursively extract referenced config-file.
        """
        # for chain of references
        if chain is None:
            chain = []

        # access file and read contents
        contents, fmt_ = self.get_file_contents(loc=loc, path=path)
        fmt = fmt or fmt_

        # load (recursively) from contents
        cfg = self.load_from_contents(contents, fmt=fmt, chain=chain)

        return cfg

    def load_from_contents(
        self,
        contents: bytes,
        /,
        *,
        fmt: EnumDataFileFormat,
        chain: list[tuple[EnumFilesSystem, str]] | None = None,
    ) -> T:
        """
        Extracts config from file-contents optionally parsed.

        NOTE: if `ref` attribute is set, will recursively extract referenced config-file.
        """
        # for chain of references
        if chain is None:
            chain = []

        # parse bytes -> dictionary
        assets = parse_contents(contents, format=fmt.value)

        # parse dictionary -> model
        try:
            cfg = self.type_.model_validate(assets)

        except Exception as err:
            try:
                cfg = ProxyConfig.model_validate(assets)

            except Exception as _:
                # raise first error!
                raise err

        if isinstance(proxy := cfg, ProxyConfig):
            cfg = self.load_from_proxy(proxy, chain=chain)

        return cfg

    def load_from_proxy(
        self,
        proxy: ProxyConfig,
        /,
        *,
        chain: list[tuple[EnumFilesSystem, str]] | None = None,
    ) -> T:
        """
        Extracts config from a proxy to a file.

        NOTE: if `ref` attribute is set, will recursively extract referenced config-file.
        """
        # for chain of references
        if chain is None:
            chain = []

        loc = proxy.ref.location
        path = proxy.ref.path
        fmt = proxy.ref.format
        if (loc, path) in chain:
            chain_str = ' -> '.join([f"{loc_}/{path_}" for loc_, path_ in [*chain, (loc, path)]])  # fmt: skip
            raise Exception(f"circular reference encountered whilst importing config {chain_str}!")  # fmt: skip

        # recursive call
        chain.append((loc, path))
        cfg = self.load_from_file(loc=loc, path=path, fmt=fmt, chain=chain)  # fmt: skip

        return cfg
