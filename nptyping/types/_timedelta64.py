from typing import Any, Type

import numpy
from typish import get_mro

from nptyping.types._nptype import NPType


class _Timedelta64Meta(type):
    def __repr__(cls):
        return 'Timedelta64'

    __str__ = __repr__

    def __instancecheck__(cls, instance: Any) -> bool:
        from nptyping.functions._get_type import get_type
        np_type = get_type(instance)
        return np_type == Timedelta64 and issubclass(np_type, cls)

    def __subclasscheck__(cls, subclass: type) -> bool:
        return Timedelta64 in get_mro(subclass)


class Timedelta64(NPType, numpy.timedelta64, metaclass=_Timedelta64Meta):
    """
    Corresponds to numpy.timedelta64.
    """

    @classmethod
    def type_of(cls, obj: Any) -> Type['Bool']:
        """
        Return the NPType that corresponds to obj.
        :param obj: a string compatible object.
        :return: a Timedelta64 type.
        """
        from nptyping.functions._get_type import get_type_timedelta64
        return get_type_timedelta64(obj)
