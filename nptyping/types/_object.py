from typing import Any

import numpy

from nptyping.types._nptype import NPType


class _ObjectMeta(type):
    def __repr__(cls):
        return 'Object'

    def __subclasscheck__(cls, other: Any) -> bool:
        return True

    __str__ = __repr__
    __instancecheck__ = __subclasscheck__


class Object(NPType, numpy.generic, metaclass=_ObjectMeta):
    """
    Corresponds to numpy.object.
    """
