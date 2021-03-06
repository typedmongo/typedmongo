from inspect import isclass
from typing import Any, Generic, NoReturn, Tuple, TypeVar, Union


def snake_case(name: str) -> str:
    """
    convert "SomeWords" to "some_words"
    """
    return "".join(
        "_" + char.lower() if char.isupper() and i > 0 else char.lower()
        for i, char in enumerate(name)
    )


def assert_type(name: str, variable: object, expected_type: object, nullable=True):
    if nullable and variable is None:
        return
    if not isinstance(variable, expected_type):
        raise TypeError(f'The {name} argument should be {expected_type.__name__} type')


class OnlyUseAsClass(type):
    def __call__(self, *args, **kwds) -> NoReturn:
        raise NotImplementedError(
            f"The class {self.__name__} cannot be instantiated, please use it directly."
        )


def safe_issubclass(
    obj: Any, class_or_tuple: Union[type, Tuple[Union[type, Tuple[Any, ...]], ...]]
) -> bool:
    return isclass(obj) and issubclass(obj, class_or_tuple)


T = TypeVar("T")


class ImmutableAttribute(Generic[T]):
    def __set_name__(self, owner: object, name: str) -> None:
        self.public_name = name
        self.private_name = "_" + name

    def __get__(self, instance: object, cls: type = None) -> T:
        return getattr(instance, self.private_name)

    def __set__(self, instance: object, value: T) -> None:
        if hasattr(instance, self.private_name):
            raise RuntimeError(
                f"{instance.__class__.__name__}.{self.public_name} is immuSchema"
            )
        setattr(instance, self.private_name, value)

    def __delete__(self, instance: object) -> None:
        raise RuntimeError(
            f"{instance.__class__.__name__}.{self.public_name} is immuSchema"
        )
