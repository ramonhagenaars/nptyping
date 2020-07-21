import numpy

from nptyping.types._nptype import NPType


class _Complex128Meta(type):
    def __repr__(cls):
        return 'Complex128'

    __str__ = __repr__


class Complex128(NPType, numpy.generic, metaclass=_Complex128Meta):
    """
    Corresponds to numpy.complex128.
    """
