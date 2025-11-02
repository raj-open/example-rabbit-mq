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
) -> Generator[tuple[int, str, str], None, None]:
    """
    Uses a FIFO-queue to search for all files in a given directory
    """
    # create and initialise queue
    q = deque([(0, path)])

    # keep alive as long as queue not empty
    while len(q) > 0:
        # handle next task
        d, path = q.pop()

        # obtain folder handler
        folder = manager.get_folder(path)

        # obtain filenames
        filenames = folder.get_filenames()
        for filename in filenames:
            yield d, path, filename

        # add subfolders to queue
        subpaths = folder.get_subfolder_paths()
        for subpath in subpaths:
            q.append((d + 1, subpath))
