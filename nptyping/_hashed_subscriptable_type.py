from typing import Any, Dict

from typish import SubscriptableType


class HashedSubscriptableType(SubscriptableType):
    _cache = {}

    def __getitem__(cls, item: Any) -> Any:
        # Take the item's class name into account to distinguish between
        # e.g. ints and floats.
        hashed = hash('{}{}{}'.format(
            cls.__name__, item.__class__.__name__, item))
        if hashed not in cls._cache:
            cls._cache[hashed] = SubscriptableType.__getitem__(cls, item)
        result = cls._cache[hashed]
        return result