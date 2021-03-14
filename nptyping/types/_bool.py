from typing import Any, Type

import numpy
from typish import get_mro

from nptyping.types._nptype import NPType


class _BoolMeta(type):
    def __repr__(cls):
        return 'Bool'

    __str__ = __repr__

    def __instancecheck__(cls, instance: Any) -> bool:
        from nptyping.functions._get_type import get_type
        np_type = get_type(instance)
        return np_type == Bool and issubclass(np_type, cls)

    def __subclasscheck__(cls, subclass: type) -> bool:
        return Bool in get_mro(subclass)


class Bool(NPType, numpy.bool_, metaclass=_BoolMeta):
    """
    Corresponds to numpy.bool_.
    """

    @classmethod
    def type_of(cls, obj: Any) -> Type['Bool']:
        """
        Return the NPType that corresponds to obj.
        :param obj: a string compatible object.
        :return: a Unicode type.
        """
        from nptyping.functions._get_type import get_type_bool
        return get_type_bool(obj)
