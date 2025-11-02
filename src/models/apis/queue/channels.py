#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import logging

from pika import BlockingConnection
from pika import ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import SkipValidation

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "ChannelContext",
]

# ----------------------------------------------------------------
# CLASSES
# ----------------------------------------------------------------


class ChannelStruct(BaseModel):
    """
    A struct which contains settings + dynamically determined properties of channel
    """

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    settings: SkipValidation[ConnectionParameters]
    channel: SkipValidation[BlockingChannel] | None = None


class ChannelContext(ChannelStruct):
    """
    Provides a Channel as a context manager
    """

    def __enter__(self) -> BlockingChannel:
        with BlockingConnection(self.settings) as connection:
            self.channel = connection.channel()
            return self.channel

    def __exit__(self, *_, **__):
        logging.info("gracefully terminating channel")
        if self.channel is not None:
            self.channel.close()
        return
