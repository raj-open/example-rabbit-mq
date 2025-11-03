#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from argparse import ArgumentParser

from ..._core.utils.misc import *
from ...models.application import *
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
    _prog = "src/cli.py"
    _part = "APPLICATION"

    def create_parser(self) -> ArgumentParser:
        parser = self.base_parser
        parser.add_argument(
            "mode",
            type=EnumFeatures,
            choices=[e.value for e in EnumFeatures],
            help=dedent_full(
                f"""
                {EnumFeatures.VERSION.value} = show version of programme
                {EnumFeatures.SEARCH_FS.value} = runs feature that searches a filesystem
                """
            ),
        )
        parser.add_argument(
            "--config",
            type=str,
            nargs="?",
            help="set default path to general config",
            default="setup/config.yaml",
        )
        parser.add_argument(
            "--requests",
            nargs="?",
            type=str,
            help="Set default path to requests payload",
            default="setup/requests.yaml",
        )
        parser.add_argument(
            "--env",
            nargs="?",
            type=str,
            help="path to environment file",
            default=".env",
        )
        parser.add_argument(
            "--log",
            nargs="?",
            type=str,
            help="path to files for logging",
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="more verbose console logging (force logging level to be DEBUG)",
        )
        return parser
