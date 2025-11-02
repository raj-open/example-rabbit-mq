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
def ChannelContext(settings: ConnectionParameters, /) -> Generator[BlockingChannel]:
    """
    Provides a Channel as a context manager
    """
    with BlockingConnection(settings) as connection:
        chan = connection.channel()
        yield chan
        logging.info("gracefully terminating channel")
        chan.close()
