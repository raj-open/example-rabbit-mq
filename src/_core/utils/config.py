#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

import yaml

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "YamlIndentDumper",
]

# ----------------------------------------------------------------
# METHODS
# ----------------------------------------------------------------


class YamlIndentDumper(yaml.Dumper):
    """
    PyYaml's `yaml.dump` for lists yields
    ```yaml
    key:
    - value1
    - value2
    - ...
    ```
    which currently does not match standard style, i.e.
    ```yaml
    key:
      - value1
      - value2
      - ...
    ```
    This class fixes this issue.

    Usage
    ```py
    yaml.dump(..., Dumper=YamlIndentDumper)
    ```
    """

    def increase_indent(
        self,
        flow=False,
        indentless=False,
    ):
        return super(YamlIndentDumper, self).increase_indent(flow, False)
