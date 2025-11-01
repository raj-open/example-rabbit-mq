#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import re
import time
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import overload
from zoneinfo import ZoneInfo

import pytz
from codetiming import Timer as TimerBasic
from pydantic import AwareDatetime
from pydantic import BaseModel
from pydantic import ConfigDict
from tzlocal import get_localzone

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "Timer",
    "add_timezone",
    "get_date_stamp",
    "get_datetime_stamp",
    "get_local_timezone",
    "get_timestamp",
    "get_timezone_from_name",
    "parse_datetime",
    "parse_duration",
    "remove_timezone",
    "timezone_as_gmt_offset",
]

# ----------------------------------------------------------------
# LOCAL VARIABLES
# ----------------------------------------------------------------

_TIME_PATTERN = re.compile(pattern=r"^(.*)([\+-])(\d+\:\d+)$")

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def parse_datetime(stamp: str) -> datetime:
    return datetime.fromisoformat(stamp.replace("Z", " +00:00"))


def get_timestamp(format: str = r"%Y-%m-%d %H:%M:%S%z") -> str:
    return datetime.now().strftime(format)


def get_datetime_stamp(rounded: bool = False) -> str:
    return get_timestamp(r"%Y-%m-%d %H:%M:%S%z" if rounded else r"%Y-%m-%d %H:%M:%S.%f%z")


def get_date_stamp() -> str:
    return get_timestamp(r"%Y-%m-%d")


def get_local_timezone() -> timezone:
    """
    Returns the system timezone
    """
    zone = get_localzone()
    tz = get_timezone_from_name(zone)
    return tz


def get_timezone_from_name(zone: str | ZoneInfo, /) -> timezone:
    """
    Given a timezone as name e.g. UTC, CET, Asia/Tokyo, UTC+02:00
    determines a standard timezone.
    """
    text = str(zone)
    tz_file = pytz.timezone(text)
    dt = datetime.now(tz_file).utcoffset() or timedelta()
    tz = timezone(dt)
    return tz


def timezone_as_gmt_offset(tz: timezone) -> str:
    """
    Determines a universally acceptable format
    for a timezone name.
    """
    # compute offset as hours
    t = datetime.now(tz)
    dt = t.utcoffset()
    offset = dt.total_seconds() / 3600
    hours = round(offset)

    if offset > 0:
        return f"Etc/GMT+{hours:d}"

    elif offset < 0:
        return f"Etc/GMT-{-hours:d}"

    return "GMT"


class Timer(TimerBasic):
    _pause_time: float

    def start(self):
        """
        Starts the timer.
        """
        super().start()
        self._pause_time = self._start_time

    @property
    def laptime(self) -> float:
        """
        Computes the time duration since last "lap"
        (or since start of this is the first lap).

        NOTE: Does not pause or reset the timer.
        """
        t0 = self._pause_time
        t1 = time.perf_counter()
        self._pause_time = t1
        return t1 - t0

    @property
    def elapsed(self) -> float:
        """
        Returns the time duration since start.

        NOTE: Does not pause or reset the timer.
        """
        self.last = time.perf_counter() - self._start_time
        return self.last


@overload
def remove_timezone(t: None, /) -> None: ...


@overload
def remove_timezone(t: datetime, /) -> datetime: ...


def remove_timezone(t: datetime | None, /) -> datetime | None:
    """
    Places in UTC and removes timezone information.
    """
    match t:
        case datetime():
            if t.tzinfo is not None:
                t = t.astimezone(tz=timezone.utc)
                t = t.replace(tzinfo=None)

            return t

        case _:
            return None


@overload
def add_timezone(
    t: None,
    /,
    *,
    tz: timezone = timezone.utc,
) -> None: ...


@overload
def add_timezone(
    t: datetime,
    /,
    *,
    tz: timezone = timezone.utc,
) -> AwareDatetime: ...


def add_timezone(
    t: datetime | None,
    /,
    *,
    tz: timezone = timezone.utc,
) -> AwareDatetime | None:
    """
    Adds timezone, ensuring UTC.
    """
    match t:
        case datetime():
            if t.tzinfo is None:
                t = t.replace(tzinfo=tz)

            else:
                t = t.astimezone(tz=tz)

            return t

        case _:
            return None


@overload
def parse_duration(expr: str, /) -> timedelta: ...


@overload
def parse_duration(expr: None, /) -> None: ...


def parse_duration(expr: str | None) -> timedelta | None:
    """
    Computes time duration based on a string expression
    """

    class TimeDuration(BaseModel):
        model_config = ConfigDict(
            extra="allow",
            populate_by_name=True,
        )
        value: timedelta | None

    try:
        obj = TimeDuration.model_validate({"value": expr})
        return obj.value

    except Exception as _:
        return None
