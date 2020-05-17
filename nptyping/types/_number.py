from typing import Any, Union, Type

import numpy
from typish import Literal

from nptyping import py_type
from nptyping.types._nptype import NPType, SimpleNPTypeMeta


class _NumberMeta(SimpleNPTypeMeta):
    """
    Super metaclass for the Number class.
    """
    def __instancecheck__(cls, instance: Any) -> bool:
        npbase = getattr(cls, 'npbase', None)
        if not npbase:
            try:
                return py_type(instance) in (int, float)
            except ValueError:
                return False
        # This instance check simply relies on the numpy instance check.
        return isinstance(instance, npbase)

    def __subclasscheck__(cls, subclass: type) -> bool:
        return (isinstance(subclass, Number)
                and not cls.npbase or issubclass(subclass.npbase, cls.npbase))


class Number(NPType, metaclass=_NumberMeta):
    """
    Superclass for number types (integers and floating point numbers). Can be
    optionally given the number of bits.
    """
    npbase = None

    @classmethod
    def _after_subscription(cls, args: Any) -> None:
        if isinstance(args, tuple):
            cls.base = args[0]
            cls.npbase = args[1]
            return

        if not isinstance(args, int):
            raise TypeError('Number takes only an int as generic type. '
                            'Given: {}'.format(type(args).__name__))

        cls.npbase = getattr(numpy, '{}{}'.format(cls.base.__name__, args),
                             None)
        if not cls.npbase:
            raise TypeError('Unsupported number of bits: {}'.format(args))

    @classmethod
    def bits(cls) -> Union[int, Literal[Any]]:
        """
        Return the number of bits of this Number type.
        :return: the number of bits or Any.
        """
        return cls.__args__ or Any


class Int(Number[int, numpy.signedinteger]):
    """
    A (signed) numpy int. Can be given the number of bits optionally.

    >>> Int[32]
    Int[32]
    """

    @staticmethod
    def of(number: int) -> Type['Int']:
        """
        Return the Int type that corresponds to the given number.
        :param number: the number of which an Int type is to be returned.
        :return: an Int type.
        """
        dtype_ = numpy.dtype(type(number))
        bits = dtype_.itemsize * 8  # Convert bytes to bits.
        return Int[bits]

    @staticmethod
    def fitting(number: int) -> Type['Int']:
        """
        Return the Int type that fits the given number.
        :param number: the number of which the Int type is to be found.
        :return: a type of Int.
        """
        bitlen = number.bit_length()
        for bits in [8, 16, 32, 64]:
            if bitlen <= bits - 1:  # subtract sign bit.
                return Int[bits]


class UInt(Number[int, numpy.unsignedinteger]):
    """
    An unsigned numpy int. Can be given the number of bits optionally.

    >>> UInt[32]
    UInt[32]
    """

    @staticmethod
    def fitting(number: int) -> Type['UInt']:
        """
        Return the UInt type that fits the given number.
        :param number: the number of which the UInt type is to be found.
        :return: a type of UInt.
        """
        bitlen = number.bit_length()
        for bits in [8, 16, 32, 64]:
            if bitlen <= bits:
                return UInt[bits]


class Float(Number[float, numpy.floating]):
    """
    A numpy float. Can be given the number of bits optionally.

    >>> Float[32]
    Float[32]
    """


Int8 = Int[8]
Int16 = Int[16]
Int32 = Int[32]
Int64 = Int[64]

UInt8 = UInt[8]
UInt16 = UInt[16]
UInt32 = UInt[32]
UInt64 = UInt[64]

Float16 = Float[16]
Float32 = Float[32]
Float64 = Float[64]
