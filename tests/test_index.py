import pytest

from typedmongo import Index


def test_json():
    assert Index().value == {}
    assert Index(unique=True).value == {"unique": True}
    assert Index(sparse=True).value == {"sparse": True}
    assert Index(expire=600).value == {"expireAfterSeconds": 600}
    assert Index(unique=True, sparse=True, expire=600).value == {
        "unique": True,
        "sparse": True,
        "expireAfterSeconds": 600,
    }


def test_keys():
    assert Index(keys={}).keys == {}
    assert Index(keys={"hello": 1}).keys == {"hello": 1}
    assert Index().add_key("hello", -1).keys == {"hello": -1}

    # Not override able
    assert Index().add_key("hello", -1).add_key("hello", 1).keys == {"hello": -1}

    with pytest.raises(TypeError):
        Index(keys={"hello": 2})
    with pytest.raises(TypeError):
        Index(keys={123: 2})
    with pytest.raises(TypeError):
        Index(keys={"hello": "123"})
    with pytest.raises(TypeError):
        Index().add_key("hello", 100)
