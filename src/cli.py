#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Entry point to run application via CLI
"""

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import os
import sys
from pathlib import Path

os.chdir(Path(__file__).parent.parent)
sys.path.insert(0, os.getcwd())

from ._core.logging import *
from ._core.utils.basic import *
from .features import *
from .models.application import *
from .queries import *
from .queries._console.cli import *
from .setup import *

# ----------------------------------------------------------------
# LOCAL CONSTANTS
# ----------------------------------------------------------------

PID = os.getpid()

# ----------------------------------------------------------------
# EXECUTION
# ----------------------------------------------------------------

if __name__ == "__main__":
    args = CliArguments(config.INFO).parse(*sys.argv[1:])

    # handle simple endpoints immediately
    if args.mode == EnumFeatures.VERSION:
        print(config.VERSION)
        exit(0)

    config.pid.set(PID)
    config.path_env.set(args.env)
    config.path_logging.set(args.log)
    config.path_config.set(args.config)
    config.path_requests.set(args.requests)
    config.initialise_application(
        name="app",
        serialise=False,
        log_to_files=True,
        verbose=args.verbose,
    )

    match args.mode:
        case EnumFeatures.SEARCH_FS:
            payload = config.parser_requests().parse()
            tasks = parse_tasks(payload)
            feat_searchfs.superfeature(tasks)

        case _ as mode:
            raise NotImplementedError(f"no feature implemented for {extract_string(mode)}")
