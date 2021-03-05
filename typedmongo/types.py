import bson
from typing import List, Union, Any
from functools import wraps


TRANSFORM_TYPES = {}


def register(transform: Union[object, List[object]] = []):
    if not isinstance(transform, list):
        transform = [transform]

    def decorator(cls: object):
        TRANSFORM_TYPES[cls] = transform
        return cls
    return decorator


class BasicType:
    _value: Any = None

    @ property
    def value(self):
        return self._value

@ register(str)
class ObjectId(str, BasicType):
    def __init__(self, value):
        try:
            self._value = bson.objectid.ObjectId(value)
        except:
            raise TypeError(f"{value} is not a valid ObjectID")


@ register(str)
class UUID(str, BasicType):
    def __init__(self, value):
        try:
            self._uuid = bson.uuid.UUID(value)
        except:
            raise TypeError(f"{value} is not a valid UUID")


@ register(str)
class Decimal128(str, BasicType):
    def __init__(self, value):
        try:
            self._decimal = bson.Decimal128(value)
        except:
            raise TypeError(f"{value} is not a valid Decimal")


@ register(object)
class AnyType(BasicType):
    def __init__(self, value):
        self._value = value

