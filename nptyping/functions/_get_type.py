from typing import Any, Type, Dict

import numpy
from typish import ClsFunction, T

from nptyping.functions._py_type import py_type
from nptyping.types._ndarray import NDArray
from nptyping.types._nptype import NPType
from nptyping.types._number import Int, Float, UInt, Number

_default_int_bits = numpy.dtype(int).itemsize * 8
_default_float_bits = numpy.dtype(float).itemsize * 8


def get_type(obj: Any) -> Type['NPType']:
    """
    Return the nptyping type of the given obj. The given obj can be a numpy
    ndarray, a dtype or a Python type. If no corresponding nptyping type
    can be determined, a TypeError is raised.
    :param obj: the object for which an nptyping type is to be returned.
    :return: a subclass of NPType.
    """
    function = ClsFunction([
        (type, _get_type_type),
        (int, Int.type_of),
        (float, Float.type_of),
        (str, lambda *_: str),  # FIXME: replace with a proper type asap.
        (numpy.dtype, _get_type_dtype),
        (numpy.ndarray, _get_type_arrary),
        (numpy.signedinteger, Int.type_of),
        (numpy.unsignedinteger, UInt.type_of),
        (numpy.floating, Float.type_of),
    ])

    if not function.understands(obj):
        raise TypeError('Type "{}" not understood.'.format(type(obj).__name__))

    return function(obj)


def _get_type_type(type_: type) -> Type['NPType']:
    # Return the nptyping type of a type.

    delegates = [
        (NPType, lambda x: x),
        (str, lambda x: x),  # FIXME: replace with a proper type asap.
        (int, Int.type_of),
        (float, Float.type_of),
        (numpy.signedinteger, Int.type_of),
        (numpy.unsignedinteger, UInt.type_of),
        (numpy.floating, Float.type_of),
    ]

    for super_type, delegate in delegates:
        if issubclass(type_, super_type):
            return delegate(type_)

    raise TypeError('Type "{}" not understood.'.format(type_.__name__))


def _get_type_dtype(dtype: numpy.dtype) -> Type['NPType']:
    # Return the nptyping type of a numpy dtype.
    if py_type(dtype) == str:  # FIXME: use proper nptyping type for strings.
        return str
    np_type_per_py_type = {
        int: Int,
        float: Float,
    }
    bits = dtype.itemsize * 8
    cls = np_type_per_py_type[(py_type(dtype))]
    return cls[bits]


def _get_type_arrary(arr: numpy.ndarray) -> Type['NPType']:
    # Return the nptyping type of a numpy array.
    type_ = get_type(arr.dtype)
    return NDArray[arr.shape, type_]


def _get_type_of_number(
        cls: Type['Number'],
        obj: Any,
        bits_per_type: Dict[type, int]) -> T:
    # Return the nptyping Number type of the given obj using cls and
    # bits_per_type.
    bits = bits_per_type.get(obj) or bits_per_type.get(type(obj))

    if not bits:
        raise TypeError('Unsupported type {} for {}'
                        .format(type(obj).__name__, cls))

    return cls[bits]


# Library private.
def get_type_int(obj: Any):
    return _get_type_of_number(Int, obj, {
        numpy.int8: 8,
        numpy.int16: 16,
        numpy.int32: 32,
        numpy.int64: 64,
        int: _default_int_bits,
    })


# Library private.
def get_type_uint(obj: Any):
    return _get_type_of_number(UInt, obj, {
        numpy.uint8: 8,
        numpy.uint16: 16,
        numpy.uint32: 32,
        numpy.uint64: 64,
        int: _default_int_bits,
    })


# Library private.
def get_type_float(obj: Any):
    return _get_type_of_number(Float, obj, {
        numpy.float16: 16,
        numpy.float32: 32,
        numpy.float64: 64,
        float: _default_float_bits,
    })
