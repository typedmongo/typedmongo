from typing import Dict

from .utils import assert_type


class Index:
    _keys: Dict[str, int] = {}

    def __init__(
        self,
        unique: bool = False,
        sparse: bool = False,
        expire: int = 0,
        name: str = None,
        keys: Dict[str, int] = None,
    ):
        assert_type("unique", unique, bool)
        assert_type("sparse", sparse, bool)
        assert_type("expire", expire, int)
        assert_type("name", name, str, True)
        assert_type("keys", keys, dict, True)
        if keys is not None:
            for k, v in keys.items():
                assert_type("keys.key", k, str)
                assert_type("keys.value", v, int)
                if v not in [1, -1]:
                    raise TypeError("The keys.value argument should be 1 or -1")

        self.unique = unique
        self.sparse = sparse
        self.expire = expire
        self.name = name
        if keys is not None:
            self._keys = keys

    @property
    def value(self):
        data = {}
        if self.unique:
            data["unique"] = True
        if self.sparse:
            data["sparse"] = True
        if self.expire != 0:
            data["expireAfterSeconds"] = self.expire
        if self.name:
            data["name"] = self.name
        return data

    def add_key(self, key, sort=1):
        assert_type("key", key, str)
        assert_type("sort", sort, int)
        if sort not in [1, -1]:
            raise TypeError("The sort argument should be 1 or -1")

        self._keys[key] = sort
        return self

    @property
    def keys(self):
        return self._keys
