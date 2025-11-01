#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to check if current time matches a given CRON expression
"""

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import datetime
import sys
from argparse import ArgumentParser
from argparse import ArgumentTypeError
from argparse import RawTextHelpFormatter
from datetime import datetime
from functools import partial

from croniter import croniter

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def parse_args(*args: str):
    parser = ArgumentParser(
        prog="cron validator",
        description="validates cron expressions and checks if current time matches cron expression",
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "cron",
        type=partial(validate_cron_expression),
        help="a cron expression (minutes|hours|day-of-month|month|day-of-week)",
    )
    parser.add_argument(
        "--time",
        type=validate_datetime_to_minute,
        help="time otherwise defaults to current time",
    )
    args_parsed = parser.parse_args(args)
    return args_parsed


def validate_cron_expression(value: str, /) -> str:
    """
    Regex validator
    """
    if not croniter.is_valid(value):
        raise ArgumentTypeError(f"'{value}' is not a valid CRON expression")

    return value


def validate_datetime_to_minute(value: str, /) -> datetime:
    """
    safely parses datetime expression
    """
    try:
        return datetime.fromisoformat(value)

    except Exception as _:
        return None


# ----------------------------------------------------------------
# EXECUTION
# ----------------------------------------------------------------

if __name__ == "__main__":
    sys.tracebacklimit = 0

    # immediately get current time
    t_now = datetime.now()

    # parse cli args
    args = parse_args(*sys.argv[1:])
    expr = args.cron
    t = (args.time or t_now).replace(second=0, microsecond=0)

    # validate timestamp against cron expression
    if not croniter.match(cron_expression=expr, testdate=t):
        raise ValueError(f"current time {t} does not match cron expression '{expr}'")
