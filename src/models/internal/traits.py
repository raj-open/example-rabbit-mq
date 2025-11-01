#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from contextvars import ContextVar
from typing import Any
from typing import Callable
from typing import Generic
from typing import TypeVar

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import SkipValidation

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "Property",
    "TriggerProperty",
]

# ----------------------------------------------------------------
# LOCAL CONSTANTS
# ----------------------------------------------------------------

T = TypeVar("T")

# ----------------------------------------------------------------
# CLASSES
# ----------------------------------------------------------------


class Property(BaseModel, Generic[T]):
    """
    A class allowing delayed setting of properties.

    Property clases are type-annotated

    ```py
    temperature = Property[float](label="temp") # property of type <float>
    ...
    value = temperature() # variable 'value' shows up with intellisense as type <float>
    ```

    To set and get value, use as follows

    ```py
    temperature = Property[float](label="temp")
    temperature.set(273.15)
    value = temperature()
    print(value) # 273.15
    ```

    Property instances are not final, i.e. can be set multiple times

    ```py
    temperature = Property[float](label="temp")
    temperature.set(273.15)
    temperature.set(0.15) # allowed
    ```

    Can set a factory method

    ```py
    name = Property[str](label="name", factory=lambda: 'Max Mustermann')
    Property(value) # 'Max Mustermann'
    ```

    If a factory method is set,
    then setting the value can still override it:

    ```py
    # .set takes precedence
    name = Property[str](label="name", factory=lambda: 'Max Mustermann')
    name.set('Julia Musterfrau')
    print(name()) # 'Julia Musterfrau'

    # .set overrides factory value
    name = Property[str](label="name", factory=lambda: 'Max Mustermann')
    print(name()) # 'Max Mustermann'
    name.set('Julia Musterfrau') # allowed
    print(name()) # 'Julia Musterfrau'
    ```
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    label: str
    default: SkipValidation[T] | None = Field(default=None)
    factory: SkipValidation[Callable[[], T]] | None = Field(default=None)
    value: SkipValidation[ContextVar[T]] = Field(
        default_factory=lambda: ContextVar[T]("name"),
        init=False,
    )

    def model_post_init(self, __context: Any) -> None:
        self.value = ContextVar[T](self.label)

    def get_default(self) -> T:
        if callable(self.factory):
            return self.factory()

        if self.default is not None:
            return self.default

        raise LookupError(f"Property {self.label} unset. Call {self.label}.set(...) first!")  # fmt: skip

    def __call__(self) -> T:
        return self.get()

    def get(self) -> T:
        try:
            value = self.value.get()
            return value

        except LookupError as _:
            value = self.get_default()
            self.set(value)
            return value

    def set(self, x: T):
        self.value.set(x)


class TriggerProperty:
    """
    Use to set a boolean value to `true` and maintain this value.
    Initialises as false.
    """

    def __init__(self):
        self._value = ContextVar[bool]("trigger")
        self._value.set(False)

    @property
    def value(self):
        return self._value.get()

    def __call__(self) -> bool:
        return self._value.get()

    def set(self):
        """
        Permanently sets trigger value to `true`.
        """
        self._value.set(True)
