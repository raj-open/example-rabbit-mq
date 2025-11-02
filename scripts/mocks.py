#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to generate a local mock directory
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
import math
import random
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter

from lorem_text import lorem
from mimesis import Generic

from src._core.constants import *
from src._core.logging import *

# ----------------------------------------------------------------
# SETTINGS
# ----------------------------------------------------------------

gen = Generic()

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def parse_args(*args: str):
    parser = ArgumentParser(
        prog="mocks",
        description="creates a local mock directory for the feature SEARCH-FS",
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "--path",
        type=str,
        help="absolute or relative path to directory to be created",
        # nargs="?",
        # default="data/example",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        help="maximum depth of folders",
        # nargs="?",
        # default=4,
    )
    parser.add_argument(
        "--max-folders",
        type=int,
        help="maximum count files count",
        # nargs="?",
        # default=100,
    )
    parser.add_argument(
        "--max-files",
        type=int,
        help="maximum count files count",
        # nargs="?",
        # default=1000,
    )
    logging.info(args)
    args_parsed = parser.parse_args(args)
    return args_parsed


def create_folder(
    path: str,
    /,
    *,
    depth: int,
    k_folders: int,
    k_files: int,
):
    """
    Recursive depth-first method to create folders and files
    """
    # ensure folder exists
    logging.info(f"- create folder '{path}'")
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)

    # generate random file names
    k = random.randint(1, k_files)
    basenames = [gen.food.dish() for _ in range(k)]
    extension = random.choices([".txt", ".csv", ".md"], k=k)
    filenames = [f"{x}{ext}" for x, ext in zip(basenames, extension)]

    # create files and contents
    for filename in filenames:
        path_ = os.path.join(path, filename)
        content = lorem.paragraph().encode()
        logging.info(f"- create file '{filename}' with {len(content)/SIZE_1_KB:.4f} kb of data")  # fmt: skip

        p = Path(path_)
        p.touch(exist_ok=True)
        with open(path_, "wb") as fp:
            fp.write(content)

    # if depth remaining is 0 stop
    if depth == 0:
        return

    # otherwise proceed
    k = random.randint(1, k_folders)
    foldernames = [gen.address.city() for _ in range(k)]

    for foldername in foldernames:
        path_ = os.path.join(path, foldername)
        create_folder(
            path_,
            depth=depth - 1,
            k_folders=k_folders,
            k_files=k_files,
        )

    return


# ----------------------------------------------------------------
# EXECUTION
# ----------------------------------------------------------------

if __name__ == "__main__":
    sys.tracebacklimit = 0

    # initialise logging
    configure_logging(name="root", level="INFO", path=None, serialise=False)

    # parse the args
    args = parse_args(*sys.argv[1:])

    path = args.path
    depth = args.max_depth
    count_files = args.max_files
    count_folder = args.max_folders

    # derive how many files/subfolders per folder using heuristics
    k_folders = 0
    if depth > 1:
        k_folders = math.ceil(math.pow(count_folder, 1 / depth))

    k_files = math.ceil(count_files / count_folder)
    k_files = max(1, k_files)

    # call the recursive method
    create_folder(
        path,
        depth=depth,
        k_folders=k_folders,
        k_files=k_files,
    )
