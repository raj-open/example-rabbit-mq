#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module contains interfaces/types
"""

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from __future__ import annotations

from typing import Protocol

from pydantic import AwareDatetime

from ..._core.constants import *
from ..generated.application import MetaData

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "FilesManager",
    "FilesManagerFile",
    "FilesManagerFolder",
]

# ----------------------------------------------------------------
# CLASSES
# ----------------------------------------------------------------


class FilesManager(Protocol):
    """
    Interface for a generic file system manager
    """

    @staticmethod
    def path_split(path: str, /) -> tuple[str, str, str]:
        """
        Splits a full path into (absolute directory, basename, ext).
        """
        ...

    @staticmethod
    def path_split_root(path: str, /) -> tuple[str, str]:
        """
        Splits a full path into (root, relative path).
        """
        ...

    @staticmethod
    def path_join(*path: str) -> str:
        """
        Static method to combine parts of path
        """
        ...

    @staticmethod
    def path_rel(root: str, path: str, /) -> list[str]:
        """
        Static method to compute series of subpaths from a root to a given path
        """
        ...

    def get_folder(self, *path: str) -> FilesManagerFolder:
        """
        Use files manager to get folder by full path
        """
        ...

    def get_file(self, *path: str) -> FilesManagerFile:
        """
        Use files manager to get file by full path
        """
        ...

    def create_folder(self, path: str, /) -> FilesManagerFolder:
        """
        Use files manager to create folder by full path.
        First checks if folder already exists.
        """
        ...

    def create_file(
        self,
        contents: bytes,
        /,
        *,
        path: str,
        chunk: int = 10 * SIZE_1_MB,
    ) -> FilesManagerFile:
        """
        Use files manager to create file by full path
        """
        ...


class FilesManagerFile(Protocol):
    """
    Interface for a generic file manager
    """

    @staticmethod
    def path_split(path: str, /) -> tuple[str, str, str]:
        """
        Splits a full path into (absolute directory, basename, ext).
        """
        ...

    @staticmethod
    def path_split_root(path: str, /) -> tuple[str, str]:
        """
        Splits a full path into (root, relative path).
        """
        ...

    @property
    def exists(self) -> bool | None:
        """
        Whether or not the file exists (unknown -> `None`)
        """
        ...

    @property
    def path(self) -> str:
        """
        Gets path locator to file
        """
        ...

    @property
    def directory(self) -> str:
        """
        Gets basepath of file
        """
        ...

    @property
    def filename(self) -> str:
        """
        Gets filename of file (includes extension)
        """
        ...

    @property
    def basename(self) -> str:
        """
        Gets basename of file (excludes extension)
        """
        ...

    @property
    def ext(self) -> str:
        """
        Gets file extension
        """
        ...

    @property
    def size(self) -> int:
        """
        Gets meta attribute - size of file
        """
        ...

    @property
    def author(self) -> str | None:
        """
        Gets file author
        """
        ...

    @property
    def author_id(self) -> int | None:
        """
        Gets file author id
        """
        ...

    @property
    def date_created(self) -> AwareDatetime | None:
        """
        Gets meta attribute - date of creation
        """
        ...

    @property
    def date_modified(self) -> AwareDatetime | None:
        """
        Gets meta attribute - date of (last) modification
        """
        ...

    def get_meta_data(self) -> MetaData:
        """
        Gets bundled meta data associated to file.
        """
        ...

    def read_as_bytes(self) -> bytes:
        """
        Reads file contents to bytes
        """
        ...

    def delete_self(self) -> bool:
        """
        Deletes current file
        """
        ...


class FilesManagerFolder(Protocol):
    """
    Interface for a generic folder manager
    """

    @property
    def exists(self) -> bool | None:
        """
        Whether or not the folder exists (unknown -> `None`)
        """
        ...

    @property
    def path(self) -> str:
        """
        Gets path locator to folder
        """
        ...

    @property
    def name(self) -> str:
        """
        Gets name identifier of folder
        """
        ...

    def get_file(self, name: str, /) -> FilesManagerFile:
        """
        Gets file object by name within folder
        """
        ...

    def get_filenames(self) -> list[str]:
        """
        Get all filenames in folder
        """
        ...

    def get_files(self) -> list[FilesManagerFile]:
        """
        Gets all file objects in folder
        """
        ...

    def get_subfolder(self, name: str, /) -> FilesManagerFolder:
        """
        Gets subfolder object by name within folder
        """
        ...

    def get_subfolder_paths(self) -> list[str]:
        """
        Gets all paths to subfolders within folder
        """
        ...

    def get_subfolders(self) -> list[str]:
        """
        Gets all subfolder objects within folder
        """
        ...

    def has_file(self, file: FilesManagerFile, /) -> bool:
        """
        Checks if file of given name exists in folder
        """
        ...

    def get_files_meta_data(self) -> list[MetaData]:
        """
        Gets a list of metadata associated to files
        """
        ...

    def write_bytes(
        self,
        contents: bytes,
        /,
        *,
        name: str,
        chunk: int,
    ) -> FilesManagerFile:
        """
        Writes file contents to a folder given contents as bytes
        """
        ...

    def add_subfolder(self, name: str) -> FilesManagerFolder:
        """
        Adds subfolder and returns a manager for it.
        If subfolder already exists, it will not be created.
        """
        ...

    def clear_folder(self) -> bool:
        """
        Removes all contents of current folder
        """
        ...

    def delete_self(self) -> bool:
        """
        Deletes current folder
        """
        ...
