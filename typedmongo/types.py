from typing import Any, Dict, Generic, List, TypeVar, Union, cast

import bson

from typedmongo.utils import ImmutableAttribute

RawType = TypeVar("RawType")


class BasicType(Generic[RawType]):
    value: ImmutableAttribute[RawType]


TRANSFORM_TYPES: Dict[BasicType, List[type]] = {}


def register(transform: Union[type, List[type]]):
    if not isinstance(transform, list):
        transform = [transform]
    transform_typed = cast(List[type], transform)

    def decorator(cls: BasicType):
        TRANSFORM_TYPES[cls] = transform_typed
        return cls

    return decorator


@register(str)
class ObjectId(str, BasicType[bson.objectid.ObjectId]):
    def __init__(self, value: str) -> None:
        try:
            self.value = bson.objectid.ObjectId(value)
        except Exception:
            raise TypeError(f"{value} is not a valid ObjectID")


@register(str)
class UUID(str, BasicType[bson.uuid.UUID]):
    def __init__(self, value: str) -> None:
        try:
            self.value = bson.uuid.UUID(value)
        except Exception:
            raise TypeError(f"{value} is not a valid UUID")


@register(str)
class Decimal128(str, BasicType[bson.Decimal128]):
    def __init__(self, value: str) -> None:
        try:
            self.value = bson.Decimal128(value)
        except Exception:
            raise TypeError(f"{value} is not a valid Decimal")


@register(object)
class AnyType(BasicType):
    def __init__(self, value: Any) -> None:
        self.value = value
