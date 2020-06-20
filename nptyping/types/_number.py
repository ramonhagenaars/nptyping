from typing import Any, Union, Type

import numpy
from typish import Literal, get_mro

from nptyping.types._nptype import NPType, SimpleNPTypeMeta

DEFAULT_INT_BITS = numpy.dtype(int).itemsize * 8
DEFAULT_FLOAT_BITS = numpy.dtype(float).itemsize * 8


class _NumberMeta(SimpleNPTypeMeta):
    """
    Super metaclass for the Number class.
    """
    base = None
    npbase = None
    _bits = None
    _hashes = {}
    _repr_args = None

    def __eq__(cls, other):
        return hash(cls) == hash(other)

    def __hash__(cls):
        key = (cls.base, cls.npbase, cls._bits)
        if key not in cls._hashes:
            cls._hashes[key] = int(numpy.prod([hash(elem) for elem in key]))
        return cls._hashes[key]

    def __instancecheck__(cls, instance: Any) -> bool:
        from nptyping.functions._get_type import get_type

        if cls == instance or type(instance) in (int, float):
            # Covers Python types.
            return True

        return issubclass(get_type(instance), cls)

    def __subclasscheck__(cls, subclass: type) -> bool:
        result = False
        if cls == subclass:
            result = True
        elif _is_a(subclass, Number):
            # Cover nptyping number types.
            result = _is_number_subclass_of(subclass, cls)
        elif _is_number_type(subclass):
            result = _is_numpy_or_python_type_subclass_of(subclass, cls)
        return result


class Number(NPType, metaclass=_NumberMeta):
    """
    Superclass for number types (integers and floating point numbers). Can be
    optionally given the number of bits.
    """
    base = None
    npbase = None
    _bits = None
    _repr_args = None

    @classmethod
    def _after_subscription(cls, args: Any) -> None:
        if isinstance(args, tuple):
            cls.base = args[0]
            cls.npbase = args[1]
            return

        if not isinstance(args, int):
            raise TypeError('Number takes only an int as generic type. '
                            'Given: {}'.format(type(args).__name__))

        cls._bits = args
        cls._repr_args = args

        if not hasattr(numpy, '{}{}'.format(cls.base.__name__, cls._bits)):
            raise TypeError('Unsupported number of bits: {}'.format(args))

    @classmethod
    def bits(cls) -> Union[int, Literal[Any]]:
        """
        Return the number of bits of this Number type.
        :return: the number of bits or Any.
        """
        return cls._bits


class Int(Number[int, numpy.signedinteger]):
    """
    A (signed) numpy int. Can be given the number of bits optionally.

    >>> Int[32]
    Int[32]
    """

    @classmethod
    def type_of(cls, obj: Any) -> Type['Int']:
        """
        Return the NPType that corresponds to obj.
        :param obj: an int compatible object.
        :return: a Int type.
        """
        from nptyping.functions._get_type import get_type_int
        return get_type_int(obj)

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
                break
        return Int[bits]


class UInt(Number[int, numpy.unsignedinteger]):
    """
    An unsigned numpy int. Can be given the number of bits optionally.

    >>> UInt[32]
    UInt[32]
    """

    @classmethod
    def type_of(cls, obj: Any) -> Type['UInt']:
        """
        Return the NPType that corresponds to obj.
        :param obj: an uint compatible object.
        :return: an UInt type.
        """
        from nptyping.functions._get_type import get_type_uint
        return get_type_uint(obj)

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
                break
        return UInt[bits]


class Float(Number[float, numpy.floating]):
    """
    A numpy float. Can be given the number of bits optionally.

    >>> Float[32]
    Float[32]
    """

    @staticmethod
    def type_of(obj: Any) -> Type['Float']:
        """
        Return the NPType that corresponds to obj.
        :param obj: a float compatible object.
        :return: a Float type.
        """
        from nptyping.functions._get_type import get_type_float
        return get_type_float(obj)


def _is_a(this: Any, that: type) -> bool:
    # Return whether this is a subclass of that, considering the mro.
    return that in get_mro(this)


def _is_number_subclass_of(
        subclass: Type[Number],
        superclass: Type[Number]) -> bool:
    # Return whether subclass (which must be a type of Number) subclasses
    # superclass.
    base_is_eq = (not superclass.npbase
                  or issubclass(subclass.npbase, superclass.npbase))
    bits_is_eq = not superclass.bits() or subclass.bits() == superclass.bits()
    return base_is_eq and bits_is_eq


def _is_numpy_or_python_type_subclass_of(
        subclass: Any,
        superclass: Type[Number]) -> bool:
    # Return whether subclass (which must be a numpy type or a Python type)
    # subclasses superclass.
    if not superclass.npbase:
        # superclass is Number.
        result = True
    else:
        try:
            nptype = superclass.type_of(subclass)
        except TypeError:
            result = False
        else:
            result = issubclass(nptype, superclass)
    return result


def _is_number_type(type_: type) -> bool:
    # Return whether type_ is a numpy/Python number type.
    return (issubclass(type_, numpy.number)
            or issubclass(type_, int)
            or issubclass(type_, float))


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
