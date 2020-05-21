from typing import Any, Union, Type

import numpy
from typish import Literal, get_mro

from nptyping.functions._py_type import py_type
from nptyping.types._nptype import NPType, SimpleNPTypeMeta

_default_int_bytes = numpy.dtype(int).itemsize * 8


def _is_a(this: Any, that: type) -> bool:
    return that in get_mro(this)


class _NumberMeta(SimpleNPTypeMeta):
    """
    Super metaclass for the Number class.
    """
    base = None
    npbase = None
    bytes = None
    _hash = None

    def __eq__(cls, other):
        return hash(cls) == hash(other)

    def __hash__(cls):
        if not cls._hash:
            cls._hash = hash(cls.base) * hash(cls.npbase) * hash(cls.bytes)
        return cls._hash

    def __instancecheck__(cls, instance: Any) -> bool:
        py_number_types = (int, float)
        if type(instance) in py_number_types:
            # Covers Python types.
            return True
        if getattr(instance, 'base', None) in py_number_types:
            # Covers nptyping types.
            return True

        npbase = getattr(cls, 'npbase', None)
        if not npbase:
            # Raw nptyping.Number.
            try:
                return py_type(instance) in py_number_types
            except ValueError:
                return False

        return (instance.itemsize * 8 == cls.bytes
                and issubclass(instance.dtype.type, cls.npbase))

    def __subclasscheck__(cls, subclass: type) -> bool:

        if _is_a(subclass, Number):
            # Cover nptyping number types.
            return ((not cls.npbase or issubclass(subclass.npbase, cls.npbase))
                    and (not cls.bytes or subclass.bytes == cls.bytes))

        if (issubclass(subclass, numpy.number)
                or issubclass(subclass, int)
                or issubclass(subclass, float)):
            return not cls.npbase or cls.__subclasscheck__(cls.type_of(subclass))

        return False


class Number(NPType, metaclass=_NumberMeta):
    """
    Superclass for number types (integers and floating point numbers). Can be
    optionally given the number of bits.
    """
    base = None
    npbase = None
    bytes = None

    @classmethod
    def _after_subscription(cls, args: Any) -> None:
        if isinstance(args, tuple):
            cls.base = args[0]
            cls.npbase = args[1]
            return

        if not isinstance(args, int):
            raise TypeError('Number takes only an int as generic type. '
                            'Given: {}'.format(type(args).__name__))

        cls.bytes = args

        if not hasattr(numpy, '{}{}'.format(cls.base.__name__, cls.bytes)):
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
    def type_of(number: int) -> Type['Int']:
        """
        Return the Int type that corresponds to the given number.
        :param number: the number of which an Int type is to be returned.
        :return: an Int type.
        """
        result = {
            numpy.int8: Int8,
            numpy.int16: Int16,
            numpy.int32: Int32,
            numpy.int64: Int64,
            int: Int[_default_int_bytes],
        }.get(number)

        if not result:
            dtype_ = numpy.dtype(type(number))
            bits = dtype_.itemsize * 8  # Convert bytes to bits.
            result = Int[bits]

        return result

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
    def type_of(number: Any) -> Type['UInt']:
        """
        Return the UInt type that corresponds to the given number.
        :param number: the number of which a UInt type is to be returned.
        :return: a UInt type.
        """
        if _is_a(number, Int):
            return number

        result = {
            numpy.uint8: UInt8,
            numpy.uint16: UInt16,
            numpy.uint32: UInt32,
            numpy.uint64: UInt64,
            int: UInt[_default_int_bytes],
        }.get(number)

        if not result:
            dtype_ = numpy.dtype(type(number))
            bits = dtype_.itemsize * 8  # Convert bytes to bits.
            result = UInt[bits]

        return result

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

    @staticmethod
    def type_of(number: float) -> Type['Float']:
        """
        Return the Float type that corresponds to the given number.
        :param number: the number of which an Float type is to be returned.
        :return: an Int type.
        """
        dtype_ = numpy.dtype(type(number))
        bits = dtype_.itemsize * 8  # Convert bytes to bits.
        return Float[bits]


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
