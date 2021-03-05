import abc
from typing import Optional, Any

class Validator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def valid(self, x: Any) -> Optional[bool]:
        ...