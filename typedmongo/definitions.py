from __future__ import annotations

import inspect
from copy import deepcopy
from functools import reduce
from typing import TYPE_CHECKING, Any, Dict, Generic, Tuple, Type, TypeVar, overload, List

from .exceptions import SchemaDefineError
from .utils import ImmuSchemaAttribute, OnlyUseAsClass, snake_case
from .types import TRANSFORM_TYPES
from .validators import Required, TypeOf
from .validators.utils import Validator


FieldType = TypeVar("FieldType")


class Field(Generic[FieldType]):
    type_: ImmuSchemaAttribute[Type[FieldType]] = ImmuSchemaAttribute()

    def __init__(
        self,
        type_: Type[FieldType],
        *,
        field_name: str = "",
        not_null: bool = False,
    ) -> None:
        self.type_ = type_
        self.field_name = field_name
        self.validators = [TypeOf(self.type_)]
        self.not_null = not_null

    def __set_name__(self, owner: Schema, name: str) -> None:
        self._Schema = owner
        self._name = name

        if self.field_name == "":
            self.field_name = name

    @overload
    def __get__(self, instance: None, cls: type = None) -> Field:
        ...

    @overload
    def __get__(self, instance: object, cls: type = None) -> FieldType:
        ...

    def __get__(self, instance, cls):
        if instance is None:  # Call from class
            return self

        try:
            return instance.__dict__[self._name]
        except KeyError:
            if not self.not_null:
                return None
            raise AttributeError(f"{instance} has no attribute '{self._name}'") from None

    def __set__(self, instance: object, value: Any) -> None:
        # Type Transform
        if type(value) in TRANSFORM_TYPES.get(self.type_, []):
            value = self.type_(value)

        # Validator
        for i in self.validators:
            try:
                i.valid(value)
            except Exception as e:
                tmp = []
                for i in e.args:
                    tmp.append(i.format(name=f"{instance.__class__.__qualname__}.{self._name}", type=self.type_))
                e.args = tuple(tmp)
                raise e
        
        instance.__dict__[self._name] = value

    def __delete__(self, instance: object) -> None:
        try:
            del instance.__dict__[self._name]
        except KeyError:
            raise AttributeError(f"{instance} has no attribute '{self._name}'") from None

    def __matmul__(self, other: Any) -> Field[FieldType]:
        """
        implement a @ b
        """
        if isinstance(other, Validator):
            self.validators.append(other)
        elif issubclass(other, Validator):
            self.validators.append(other())
        else:
            return NotImplemented
        
        if isinstance(other, Required):
            self.not_null = True
        return self


class SchemaMetaClass(type):
    if TYPE_CHECKING:
        __abstract__: bool
        __Schema__: str
        __fields__: Dict[str, Field]

    def __new__(cls, name: str, bases: Tuple[type], namespace: Dict[str, Any]) -> Any:
        if "_" in name:  # check error name. e.g. Status_Info
            raise SchemaDefineError(f"Schema class name cannot have '_': {name}")
        if not name[0].isupper():  # check error name. e.g. statusInfo
            raise SchemaDefineError(f"Schema class name must be upper letter in start: {name}")

        namespace.setdefault("__abstract__", False)

        namespace.setdefault("__Schema__", snake_case(name))

        # merge bases' `__fields__` to `__fields__`
        namespace["__fields__"] = fields = reduce(
            lambda d0, d1: {**d1, **d0},
            reversed([getattr(base, "__fields__", {}) for base in bases]),
            {name: value for name, value in namespace.items() if isinstance(value, Field)},
        )

        # generate `__signature__` for calling `inspect.signature`
        namespace["__signature__"] = inspect.Signature(
            [
                inspect.Parameter(
                    name,
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    annotation=field.type_,
                )
                for name, field in fields.items()
            ],
            return_annotation=None,
        )

        return super().__new__(cls, name, bases, namespace)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if self.__abstract__:
            raise NotImplementedError(
                f"The class {self.__name__} cannot be instantiated")
        instance = super().__call__()
        for name, value in zip(instance.__fields__.keys(), args):
            setattr(instance, name, value)
        for name, value in kwargs.items():
            setattr(instance, name, value)
        return instance

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "__abstract__":
            raise AttributeError(
                "Can't modify the `__abstract__` attribute dynamically.")
        return super().__setattr__(name, value)


class Schema(metaclass=SchemaMetaClass):
    __abstract__: bool = True

    if TYPE_CHECKING:
        __Schema__: str
        __fields__: Dict[str, Field]

    def dict(self, *, copy: bool = False) -> Dict[str, Any]:
        dictionary = {k: v for k, v in self.__dict__.items() if k in self.__fields__}
        return deepcopy(dictionary) if copy else dictionary
