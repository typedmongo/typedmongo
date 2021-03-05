import abc
from typing import Any, Optional


class Validator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def valid(self, x: Any) -> Optional[bool]:
        ...
