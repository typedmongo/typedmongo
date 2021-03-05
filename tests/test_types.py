from typedmongo.definitions import Schema, Field
from typedmongo.types import ObjectId, UUID, Decimal128
from typing import List
import pytest


def test_types():
    class MySchema(Schema):
        a = Field(ObjectId)
        b = Field(UUID)
        c = Field(Decimal128)
        d = Field(int)
        
    obj = MySchema()
    obj.a = "0123456789ab0123456789ab"
    obj.b = "54133de5-ab95-4ce9-bc08-19cc6226724a"
    obj.c = "100.00"
    obj.d = 100

    assert isinstance(obj.a, ObjectId)
    assert isinstance(obj.b, UUID)
    assert isinstance(obj.c, Decimal128)
    assert isinstance(obj.d, int)

    with pytest.raises(TypeError):
        obj.a = "54133de5-ab95-4ce9-bc08-19cc6226724a"
    with pytest.raises(TypeError):
        obj.b = "0123456789ab0123456789ab"
    with pytest.raises(TypeError):
        obj.c = "0123456789ab0123456789ab"
    with pytest.raises(TypeError):
        obj.d = "0123456789ab0123456789ab"
