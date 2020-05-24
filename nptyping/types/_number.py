from typing import Any, Union, Type, Dict

import numpy
from typish import Literal, get_mro, T

from nptyping.functions._py_type import py_type
from nptyping.types._nptype import NPType, SimpleNPTypeMeta

_default_int_bits = numpy.dtype(int).itemsize * 8
_default_float_bits = numpy.dtype(float).itemsize * 8


class _NumberMeta(SimpleNPTypeMeta):
    """
    Super metaclass for the Number class.
    """
    base = None
    npbase = None
    bytes = None
    _hashes = {}

    def __eq__(cls, other):
        return hash(cls) == hash(other)

    def __hash__(cls):
        key = (cls.base, cls.npbase, cls.bytes)
        if key not in cls._hashes:
            cls._hashes[key] = int(numpy.prod([hash(elem) for elem in key]))
        return cls._hashes[key]

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
        if cls == subclass:
            return True

        if _is_a(subclass, Number):
            # Cover nptyping number types.
            return ((not cls.npbase or issubclass(subclass.npbase, cls.npbase))
                    and (not cls.bytes or subclass.bytes == cls.bytes))

        if (issubclass(subclass, numpy.number)
                or issubclass(subclass, int)
                or issubclass(subclass, float)):
            if not cls.npbase:
                # cls is Number.
                return True
            try:
                nptype = cls.type_of(subclass)
            except TypeError:
                return False
            else:
                return cls.__subclasscheck__(nptype)

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
        # FIXME: use cls.bytes
        return cls.__args__ or Any


class Int(Number[int, numpy.signedinteger]):
    """
    A (signed) numpy int. Can be given the number of bits optionally.

    >>> Int[32]
    Int[32]
    """

    @classmethod
    def type_of(cls, obj: Any) -> Type['Int']:
        return _type_of_number(Int, obj, {
            numpy.int8: 8,
            numpy.int16: 16,
            numpy.int32: 32,
            numpy.int64: 64,
            int: _default_int_bits,
        })

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

    @classmethod
    def type_of(cls, obj: Any) -> Type['UInt']:
        return _type_of_number(UInt, obj, {
            numpy.uint8: 8,
            numpy.uint16: 16,
            numpy.uint32: 32,
            numpy.uint64: 64,
            int: _default_int_bits,
        })

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
    def type_of(obj: Any) -> Type['Float']:
        return _type_of_number(Float, obj, {
            numpy.float16: 16,
            numpy.float32: 32,
            numpy.float64: 64,
            float: _default_float_bits,
        })


def _is_a(this: Any, that: type) -> bool:
    # Return whether this is a subclass of that, considering the mro.
    return that in get_mro(this)


def _type_of_number(
        cls: T,
        obj: Any,
        bits_per_type: Dict[type, int]) -> T:
    # Return the nptyping Number type of the given obj using cls and
    # bits_per_type.
    bits = bits_per_type.get(obj) or bits_per_type.get(type(obj))

    if not bits:
        raise TypeError('Unsupported type {} for {}'
                        .format(type(obj).__name__, cls))

    return cls[bits]


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
