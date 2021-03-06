from unittest import TestCase

import pytest

from typedmongo import Index


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
    TestCase().assertDictEqual(
        Index().add_key("hello", -1).add_key("hello", 1).keys, {"hello": 1}
    )

    with pytest.raises(TypeError):
        Index(keys={"hello": 2})
    with pytest.raises(TypeError):
        Index(keys={123: 2})
    with pytest.raises(TypeError):
        Index(keys={"hello": "123"})
    with pytest.raises(TypeError):
        Index().add_key("hello", 100)
