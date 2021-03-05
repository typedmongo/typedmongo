import datetime

import pytest

from typedmongo.definitions import Field, Schema
from typedmongo.validators import Max, Min, Required


def test_general():
    class MySchema(Schema):
        int_value = Field(int) @ Min(50) @ Max(300)

    obj = MySchema()
    obj.int_value = 100

    with pytest.raises(ValueError):
        obj.int_value = 30
    with pytest.raises(ValueError):
        obj.int_value = 1000


def test_required():
    class MySchema(Schema):
        required0 = Field(int) @ Required
        required1 = Field(int) @ Required()
        non_required = Field(int)

    obj = MySchema()
    obj.required0 = 30

    assert obj.non_required is None
    assert obj.required0 == 30
    with pytest.raises(AttributeError):
        obj.required1


def test_min():
    now = datetime.datetime.now()
    Min(10).valid(30)
    Min(10).valid("*" * 30)
    Min(10).valid(30.00)
    Min(now).valid(now.replace(year=3000))

    with pytest.raises(ValueError):
        Min(100).valid(30)
    with pytest.raises(ValueError):
        Min(100).valid("*" * 30)
    with pytest.raises(ValueError):
        Min(100).valid(30.00)
    with pytest.raises(ValueError):
        Min(now).valid(now.replace(year=2000))


def test_max():
    now = datetime.datetime.now()
    Max(100).valid(30)
    Max(100).valid("*" * 30)
    Max(100).valid(30.00)
    Max(now).valid(now.replace(year=2000))

    with pytest.raises(ValueError):
        Max(100).valid(130)
    with pytest.raises(ValueError):
        Max(100).valid("*" * 130)
    with pytest.raises(ValueError):
        Max(100).valid(130.00)
    with pytest.raises(ValueError):
        Max(now).valid(now.replace(year=3000))
