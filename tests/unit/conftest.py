#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import os
import sys
from pathlib import Path

os.chdir(Path(__file__).parent.parent.parent)
sys.path.insert(0, os.getcwd())

from unittest import TestCase

from pytest import fixture

# ----------------------------------------------------------------
# FIXTURES - GENERAL
# ----------------------------------------------------------------


@fixture(scope="session", autouse=True)
def test() -> TestCase:
    return TestCase()
