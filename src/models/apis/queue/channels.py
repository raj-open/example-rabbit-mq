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
from pydantic import Field
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
    connection: SkipValidation[BlockingConnection] | None = Field(default=None, init=False)
    channel: SkipValidation[BlockingChannel] | None = Field(default=None, init=False)


class ChannelContext(ChannelStruct):
    """
    Provides a Channel as a context manager
    """

    def __enter__(self) -> BlockingChannel:
        self.connection = BlockingConnection(self.settings)
        self.channel = self.connection.channel()
        return self.channel

    def __exit__(self, *_, **__):
        logging.info("gracefully terminating channel")

        if isinstance(self.channel, BlockingChannel):
            self.channel.close()

        if isinstance(self.connection, BlockingConnection):
            self.connection.close()

        return
