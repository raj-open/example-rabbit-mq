#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Entry point to serve as FastAPI-application
"""

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import os
import sys
from pathlib import Path

os.chdir(Path(__file__).parent.parent)
sys.path.insert(0, os.getcwd())

import logging

import uvicorn

from .app.endpoints_fastapi import *
from .models.application import *
from .queries import *
from .queries._console.api import *
from .setup import *

# ----------------------------------------------------------------
# LOCAL CONSTANTS
# ----------------------------------------------------------------

PID = os.getpid()
# NOTE: need this in case Azurite blob storage is connected
try:
    logger = logging.getLogger("azure.core.pipeline.policies")
    logger.setLevel(logging.WARNING)

except Exception as _:
    pass

# ----------------------------------------------------------------
# EXECUTION
# ----------------------------------------------------------------

if __name__ == "__main__":
    args = CliArguments(config.INFO).parse(*sys.argv[1:])

    config.pid.set(PID)
    config.path_env.set(args.env)
    config.path_config.set(args.config)
    config.initialise_application(
        name="app",
        serialise=False,
        log_to_files=True,
        verbose=args.verbose,
    )

    # create app
    route = ""  # NOTE: only use "/xyz" do serve multiple application on the same port
    app = create_ui(route=route, debug=args.verbose)

    # run app
    uvicorn.run(app=app, host=config.http_ip.get(), port=config.http_port.get())
