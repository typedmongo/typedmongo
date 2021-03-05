from typing import cast, Any, Dict, List, Union

import bson


class BasicType:
    _value: Any = None

    @property
    def value(self):
        return self._value


TRANSFORM_TYPES: Dict[BasicType, List[type]] = {}


def register(transform: Union[type, List[type]] = []):
    if not isinstance(transform, list):
        transform = [transform]
    transform_typed = cast(List[type], transform)

    def decorator(cls: BasicType):
        TRANSFORM_TYPES[cls] = transform_typed
        return cls

    return decorator


@register(str)
class ObjectId(str, BasicType):
    def __init__(self, value):
        try:
            self._value = bson.objectid.ObjectId(value)
        except Exception:
            raise TypeError(f"{value} is not a valid ObjectID")


@register(str)
class UUID(str, BasicType):
    def __init__(self, value):
        try:
            self._uuid = bson.uuid.UUID(value)
        except Exception:
            raise TypeError(f"{value} is not a valid UUID")


@register(str)
class Decimal128(str, BasicType):
    def __init__(self, value):
        try:
            self._decimal = bson.Decimal128(value)
        except Exception:
            raise TypeError(f"{value} is not a valid Decimal")


@register(object)
class AnyType(BasicType):
    def __init__(self, value):
        self._value = value
