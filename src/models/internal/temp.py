#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from typing import Iterable

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "TempNameGenerator",
    "temp_name",
]

# ----------------------------------------------------------------
# METHODS - STRINGS
# ----------------------------------------------------------------


class TempNameGenerator(BaseModel):
    """
    Creates a generator for unused temporary names
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    names: Iterable[str]
    name: str = Field(default="tmp")
    template: str = Field(default="tmp_{0}")
    counter_: int = Field(
        default=0,
        init=False,
    )
    used_: set[str] = Field(default_factory=set, init=False, repr=False)
    new_: set[str] = Field(default_factory=set, init=False, repr=False)

    def model_post_init(self, __context):
        self.used_ = {name for name in self.names}
        self.new_ = set()

    def get_temporary(self) -> set[str]:
        """
        Returns the newly created temp names
        """
        return self.new_

    def __call__(self) -> str:
        """
        Generate a previously unused temporary name
        """
        result = self.name

        while result in self.used_:
            self.counter_ += 1  # iterate first to ensure 1st index is 1
            result = self.template.format(self.counter_)

        self.new_.add(result)
        self.used_.add(result)

        return result


def temp_name(
    names: Iterable[str],
    /,
    *,
    name: str = "tmp",
    template: str = "tmp_{0}",
) -> str:
    gen = TempNameGenerator(names=names, name=name, template=template)
    return gen()
