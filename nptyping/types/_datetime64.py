from typing import Type, Any

import numpy
from typish import get_mro

from nptyping.types._nptype import NPType


class _Datetime64Meta(type):
    def __repr__(cls):
        return 'Datetime64'

    __str__ = __repr__

    def __instancecheck__(cls, instance: Any) -> bool:
        from nptyping.functions._get_type import get_type_datetime64
        datetime_ = get_type_datetime64(instance)
        return issubclass(datetime_, cls)

    def __subclasscheck__(cls, subclass: type) -> bool:
        return Datetime64 in get_mro(subclass)


class Datetime64(NPType, numpy.datetime64, metaclass=_Datetime64Meta):
    """
    Corresponds to numpy.datetime64.
    """

    @classmethod
    def type_of(cls, obj: Any) -> Type['Bool']:
        """
        Return the NPType that corresponds to obj.
        :param obj: a string compatible object.
        :return: a Datetime64 type.
        """
        from nptyping.functions._get_type import get_type_datetime64
        return get_type_datetime64(obj)
