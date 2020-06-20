from typing import Type, Any

import numpy
from typish import get_mro

from nptyping.types._nptype import NPType


class _Timedelta64Meta(type):
    def __repr__(cls):
        return 'Timedelta64'

    __str__ = __repr__

    def __instancecheck__(cls, instance: Any) -> bool:
        from nptyping.functions._get_type import get_type_timedelta64
        timedelta_ = get_type_timedelta64(instance)
        return issubclass(timedelta_, cls)

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
