#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import re
from contextvars import ContextVar

import yaml

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "register_yaml_constructors",
]

# ----------------------------------------------------------------
# LOCAL CONSTANTS
# ----------------------------------------------------------------

_yaml_constructors_registered = ContextVar[bool]("constructors registered", default=False)

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


def register_yaml_constructors():
    """
    Registers yaml-sugar to help parse .yaml files
    """
    if _yaml_constructors_registered.get():
        return

    yaml.add_constructor(tag="!include", constructor=include_constructor)
    yaml.add_constructor(tag="!not", constructor=not_constructor)
    yaml.add_constructor(tag="!join", constructor=join_constructor)
    yaml.add_constructor(tag="!tuple", constructor=tuple_constructor)

    _yaml_constructors_registered.set(True)
    return


# ----------------------------------------------------------------
# PARTS
# ----------------------------------------------------------------


def include_constructor(loader: yaml.Loader, node: yaml.Node):
    try:
        value = loader.construct_yaml_str(node)
        assert isinstance(value, str)
        # parse argument
        m = re.match(pattern=r"^(.*)\/#\/?(.*)$", string=value)
        # read yaml from path
        path = m.group(1) if m else value
        register_yaml_constructors()
        with open(path, "rb") as fp:
            obj = yaml.load(fp, yaml.FullLoader)
        # get part of yaml
        keys_as_str = m.group(2) if m else ""
        keys = keys_as_str.split("/")
        for key in keys:
            if key == "":
                continue
            obj = obj.get(key, dict())
        return obj

    except Exception as _:
        return None


def not_constructor(loader: yaml.Loader, node: yaml.Node) -> bool:
    try:
        value = loader.construct_yaml_bool(node)
        return not value

    except Exception as _:
        return None


def join_constructor(loader: yaml.Loader, node: yaml.Node):
    try:
        values = loader.construct_sequence(node, deep=True)
        sep, parts = str(values[0]), [str(_) for _ in values[1]]
        return sep.join(parts)

    except Exception as _:
        return ""


def tuple_constructor(loader: yaml.Loader, node: yaml.Node):
    try:
        value = loader.construct_sequence(node, deep=True)
        return tuple(value)

    except Exception as _:
        return None
