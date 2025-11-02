#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Recursive search algorithms
"""

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from collections import deque
from typing import Generator

from ...models.filesmanager import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "recursive_file_search",
]

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def recursive_file_search(
    manager: FilesManager,
    /,
    *,
    path: str,
    skip_empty: bool = False,
    max_queue_size: int = 1_000_000,
) -> Generator[tuple[int, str, str], None, None]:
    """
    Uses a FIFO-queue to search for all files in a given directory

    @inputs

    - `manager` - instance of `FilesManager` protocol for handling object in filessystem

    - `path` <`string`> - path to directory to be recursively searched

    - `skip_empty` <`boolean`>
        - if set to `true` will only search for non-empty files (faster)
        - if set to `false` will include empty files

    - `max_queue_size` <`integer`> - a safety bound to prevent out of memory exceptions

    @generates

    - `d` - current (relative) depth within directory,
        whereby `0` = level of original directory

    - `path` - path to current subdirectory

    - `filename` - filename of file-object within directory
    """
    # create and initialise queue
    q = deque[tuple[int, str | list[str]]]()
    q.append((0, path))

    # keep alive as long as queue not empty
    while (L := len(q)) > 0:
        # safeguard to prevent memory issues
        if L > max_queue_size:
            raise MemoryError(f"queue {L} exceeds maximum size permitted {max_queue_size}")

        # get next entry
        d, entry = q.pop()

        # if entry is a list of paths, resolve and continue
        if isinstance((paths := entry), list):
            for path in paths[::-1]:
                q.appendleft((d, path))
            continue

        # otherwise entry is a path
        path = entry

        # obtain folder handler
        folder = manager.get_folder(path)

        # (optional) skip if folder empty
        if skip_empty and guard_empty_folder(folder):
            continue

        # process filenames
        for filename in folder.get_filenames():
            # (optional) skip if file empty
            # NOTE: only requests file object if needed
            if skip_empty and guard_empty_file(folder, filename):
                continue

            # -> send result
            yield d, path, filename

        # process subfolders - create new tasks
        if len(paths := folder.get_subfolder_paths()) > 0:
            q.append((d + 1, paths))

    # DEV-NOTE: ensures that something is yielded for the empty case
    empty = list[tuple[int, str, str]]()
    yield from empty


# ----------------------------------------------------------------
# AUXILIARY METHODS
# ----------------------------------------------------------------


def guard_empty_folder(
    folder: FilesManagerFolder,
    /,
) -> bool:
    return folder.size == 0


def guard_empty_file(
    folder: FilesManagerFolder,
    filename: str,
    /,
) -> bool:
    file = folder.get_file(filename)
    return file.size == 0
