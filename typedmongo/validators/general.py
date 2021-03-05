import datetime
from typing import Any

from .utils import Validator


class Required(Validator):
    def valid(self, x):
        if x is None:
            raise ValueError("{name} is required")


class TypeOf(Validator):
    def __init__(self, value: Any):
        self.value = value

    def valid(self, x):
        if not isinstance(x, self.value):
            raise TypeError(f"{{name}} expects {self.value} type, but gives {type(x)}")


class Min(Validator):
    def __init__(self, value: int):
        if not isinstance(value, int) and not isinstance(value, datetime.datetime):
            raise TypeError("Min Validator only support int and datetime as argument")
        self.value = value

    def valid(self, x):
        if isinstance(x, str):
            if len(x) < self.value:
                raise ValueError(f"The length of {{name}} can't be less than {self.value}")
        elif isinstance(x, int) or isinstance(x, float):
            if x < self.value:
                raise ValueError(f"The value of {{name}} can't be less than {self.value}")
        elif isinstance(x, datetime.datetime):
            if x < self.value:
                raise ValueError(f"The datetime of {{name}} can't be earlier than {self.value}")
        else:
            raise TypeError("Type of {name} ({type}) is not supported for Min Validator")


class Max(Validator):
    def __init__(self, value: int):
        if not isinstance(value, int) and not isinstance(value, datetime.datetime):
            raise TypeError("Max Validator only support int and datetime as argument")
        self.value = value

    def valid(self, x):
        if isinstance(x, str):
            if len(x) > self.value:
                raise ValueError(f"The length of {{name}} can't be less than {self.value}")
        elif isinstance(x, int) or isinstance(x, float):
            if x > self.value:
                raise ValueError(f"The value of {{name}} can't be less than {self.value}")
        elif isinstance(x, datetime.datetime):
            if x > self.value:
                raise ValueError(f"The datetime of {{name}} can't be later than {self.value}")
        else:
            raise TypeError("Type of {name} ({type}) is not supported for Max Validator")
