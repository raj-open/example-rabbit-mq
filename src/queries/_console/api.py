#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from argparse import ArgumentParser

from .basic import *

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "CliArguments",
]

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


class CliArguments(CliArgumentsBase):
    _prog = "src/api.py"
    _part = "APPLICATION"

    def create_parser(self) -> ArgumentParser:
        parser = self.base_parser
        parser.add_argument(
            "--config",
            type=str,
            nargs="?",
            help="set default path to general config",
            default="setup/config.yaml",
        )
        parser.add_argument(
            "--env",
            nargs="?",
            type=str,
            help="path to environment file",
            default=".env",
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="more verbose console logging (force logging level to be DEBUG)",
        )
        return parser
