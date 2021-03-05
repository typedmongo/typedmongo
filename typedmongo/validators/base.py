import abc
from typing import Any


class Validator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def valid(self, x: Any) -> None:
        ...
