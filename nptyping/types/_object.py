import numpy

from nptyping.types._nptype import NPType


class _ObjectMeta(type):
    def __repr__(cls):
        return 'Object'

    __str__ = __repr__


class Object(NPType, numpy.generic, metaclass=_ObjectMeta):
    """
    Corresponds to numpy.object.
    """
