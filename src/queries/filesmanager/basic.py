#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from datetime import timezone

from ..._core.utils.basic import *
from ...models.filesmanager import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "get_files_manager",
]

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def get_files_manager(
    location: EnumFilesSystem,
    /,
    *,
    tz: timezone | None = None,
) -> FilesManager:
    """
    Obtains files manager from user choice of system location.
    """
    match location:
        case EnumFilesSystem.OS:
            return OSFilesManager(tz=tz)

        case EnumFilesSystem.SHAREPOINT:
            raise NotImplementedError("FilesManager protocol not yet implemented for Sharepoint")  # fmt: skip

        case EnumFilesSystem.BLOB_STORAGE:
            raise NotImplementedError("FilesManager protocol not yet implemented for Blobstorage")  # fmt: skip

        case _:
            raise ValueError(f"No method determined for files system manager {extract_string(location)}.")  # fmt: skip
