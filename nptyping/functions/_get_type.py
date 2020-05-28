from typing import Any, Type, Dict

import numpy
from typish import ClsFunction, T

from nptyping.functions._py_type import py_type
from nptyping.types._ndarray import NDArray
from nptyping.types._nptype import NPType
from nptyping.types._number import Int, Float, UInt, Number, DEFAULT_INT_BITS, DEFAULT_FLOAT_BITS
from nptyping.types._object import Object
from nptyping.types._unicode import Unicode


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
        (int, get_type_int),
        (float, get_type_float),
        (str, get_type_str),
        (numpy.dtype, _get_type_dtype),
        (numpy.ndarray, _get_type_arrary),
        (numpy.signedinteger, get_type_int),
        (numpy.unsignedinteger, get_type_uint),
        (numpy.floating, get_type_float),
    ])

    if not function.understands(obj):
        raise TypeError('Type "{}" not understood.'.format(type(obj).__name__))

    return function(obj)


def _get_type_type(type_: type) -> Type['NPType']:
    # Return the nptyping type of a type.

    delegates = [
        (NPType, lambda x: x),
        (str, get_type_str),
        (int, get_type_int),
        (float, get_type_float),
        (numpy.signedinteger, get_type_int),
        (numpy.unsignedinteger, get_type_uint),
        (numpy.floating, get_type_float),
    ]

    for super_type, delegate in delegates:
        if issubclass(type_, super_type):
            return delegate(type_)

    raise TypeError('Type "{}" not understood.'.format(type_.__name__))


def _get_type_dtype(dtype: numpy.dtype) -> Type['NPType']:
    # Return the nptyping type of a numpy dtype.
    np_type_per_py_type = {
        type: _get_type_type,
        int: get_type_int,
        float: get_type_float,
        str: get_type_str,
        object: lambda _: Object,
    }
    return np_type_per_py_type[(py_type(dtype))](dtype)


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
    bits = (bits_per_type.get(obj)
            or bits_per_type.get(getattr(obj, 'type', None))
            or bits_per_type.get(type(obj)))

    if not bits:
        raise TypeError('Unsupported type {} for {}'
                        .format(type(obj).__name__, cls))

    return cls[bits]


# Library private.
def get_type_str(obj: Any):
    if isinstance(obj, numpy.dtype):
        return Unicode[obj.itemsize / 4]
    if obj == str:
        return Unicode
    if not isinstance(obj, str):
        raise TypeError('Unsupported type {}'.format(type(obj)))
    return Unicode[len(obj)]


# Library private.
def get_type_int(obj: Any):
    return _get_type_of_number(Int, obj, {
        numpy.int8: 8,
        numpy.int16: 16,
        numpy.int32: 32,
        numpy.int64: 64,
        int: DEFAULT_INT_BITS,
    })


# Library private.
def get_type_uint(obj: Any):
    return _get_type_of_number(UInt, obj, {
        numpy.uint8: 8,
        numpy.uint16: 16,
        numpy.uint32: 32,
        numpy.uint64: 64,
        int: DEFAULT_INT_BITS,
    })


# Library private.
def get_type_float(obj: Any):
    return _get_type_of_number(Float, obj, {
        numpy.float16: 16,
        numpy.float32: 32,
        numpy.float64: 64,
        float: DEFAULT_FLOAT_BITS,
    })
