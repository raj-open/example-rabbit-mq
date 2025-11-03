#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import logging
from contextlib import contextmanager
from typing import Generator

from pika import BlockingConnection
from pika import ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "ChannelContext",
]

# ----------------------------------------------------------------
# CLASSES
# ----------------------------------------------------------------


@contextmanager
def ChannelContext(settings: ConnectionParameters, /) -> Generator[BlockingChannel, None, None]:
    """
    Provides a Channel as a context manager
    """
    with BlockingConnection(settings) as connection:
        try:
            chan = connection.channel()
            yield chan

        finally:
            # DEV-NOTE: this is carried out regardless of (base)exceptions - which are rethrown
            logging.info("gracefully terminating channel")
            chan.close()
