from typing import Any, Type

import numpy
from typish import get_mro

from nptyping.types._nptype import NPType, SimpleNPTypeMeta


class _UnicodeMeta(SimpleNPTypeMeta):
    def __eq__(cls, other: Any) -> bool:
        return hash(cls) == hash(other)

    def __hash__(cls: Any) -> int:
        return hash(cls.__name__) * hash(cls.chars)

    def __instancecheck__(cls, instance: Any) -> bool:
        from nptyping.functions._get_type import get_type_str
        try:
            unicode = get_type_str(instance)
        except TypeError:
            return False
        return issubclass(unicode, cls)

    def __subclasscheck__(cls, subclass: type) -> bool:
        if Unicode in get_mro(subclass):
            return cls.chars is Any or subclass.chars <= cls.chars
        return False


class Unicode(NPType, numpy.unicode, metaclass=_UnicodeMeta):
    """
    A numpy unicode. Can be given the number of characters optionally.

    >>> Unicode[50]
    Unicode[50]
    """
    chars = Any
    _repr_args = None

    @classmethod
    def _after_subscription(cls, args: Any) -> None:
        cls.chars = int(args)
        cls._repr_args = int(args)

    @classmethod
    def type_of(cls, obj: Any) -> Type['Unicode']:
        """
        Return the NPType that corresponds to obj.
        :param obj: a string compatible object.
        :return: a Unicode type.
        """
        from nptyping.functions._get_type import get_type_str
        return get_type_str(obj)
