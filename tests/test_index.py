from unittest import TestCase

import pytest

from typedmongo import Field, Index, Schema
from typedmongo.types import ObjectId


def test_json():
    TestCase().assertDictEqual(Index().value, {})
    TestCase().assertDictEqual(Index(unique=True).value, {"unique": True})
    TestCase().assertDictEqual(Index(sparse=True).value, {"sparse": True})
    TestCase().assertDictEqual(Index(expire=600).value, {"expireAfterSeconds": 600})
    TestCase().assertDictEqual(
        Index(unique=True, sparse=True, expire=600).value,
        {"unique": True, "sparse": True, "expireAfterSeconds": 600},
    )


def test_keys():
    TestCase().assertDictEqual(Index(keys={}).keys, {})
    TestCase().assertDictEqual(Index(keys={"hello": 1}).keys, {"hello": 1})
    TestCase().assertDictEqual(Index().add_key("hello", -1).keys, {"hello": -1})
    # Not override able
    TestCase().assertDictEqual(
        Index().add_key("hello", -1).add_key("hello", 1).keys, {"hello": -1}
    )

    with pytest.raises(TypeError):
        Index(keys={"hello": 2})
    with pytest.raises(TypeError):
        Index(keys={123: 2})
    with pytest.raises(TypeError):
        Index(keys={"hello": "123"})
    with pytest.raises(TypeError):
        Index().add_key("hello", 100)


def test_schema():
    class MySchema(Schema):
        pass

    MySchema.index("key", Index())
    assert MySchema.__indexes__[0].keys == {"key": 1}
    MySchema.index(Index(), key=1)
    assert MySchema.__indexes__[1].keys == {"key": 1}
    MySchema.index(Index(), key=-1)
    assert MySchema.__indexes__[2].keys == {"key": -1}

    MySchema.index("key", index=Index())
    assert MySchema.__indexes__[3].keys == {"key": 1}
    MySchema.index(key=1, index=Index())
    assert MySchema.__indexes__[4].keys == {"key": 1}
    MySchema.index(key=-1, index=Index())
    assert MySchema.__indexes__[5].keys == {"key": -1}

    MySchema.index("key0", "key1", Index())
    assert MySchema.__indexes__[6].keys == {"key0": 1, "key1": 1}
    MySchema.index(Index(), key0=1, key1=-1)
    assert MySchema.__indexes__[7].keys == {"key0": 1, "key1": -1}
    MySchema.index("key0", Index(), key1=-1)
    assert MySchema.__indexes__[8].keys == {"key0": 1, "key1": -1}
    MySchema.index("key0", key1=-1, index=Index())
    assert MySchema.__indexes__[9].keys == {"key0": 1, "key1": -1}
