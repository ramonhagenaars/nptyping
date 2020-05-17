from typing import Any

from typish import SubscriptableType


class NPType:
    """
    The baseclass of all nptyping types.
    """


class SimpleNPTypeMeta(SubscriptableType):
    """
    A metaclass for all simple NPTypes (e.g. float, int, etc.).
    """
    def __repr__(cls):
        if not cls.__args__ or cls.__args__ == Any:
            return cls.__name__
        return '{}[{}]'.format(cls.__name__, cls.__args__)

    __str__ = __repr__
