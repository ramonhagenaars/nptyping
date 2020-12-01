from datetime import datetime, timedelta
from typing import Any, Type, Dict

import numpy
from typish import ClsFunction

from nptyping.functions._py_type import py_type
from nptyping.types._bool import Bool
from nptyping.types._complex import Complex128
from nptyping.types._datetime64 import Datetime64
from nptyping.types._ndarray import NDArray
from nptyping.types._nptype import NPType
from nptyping.types._number import (
    Int,
    Float,
    UInt,
    Number,
    DEFAULT_INT_BITS,
    DEFAULT_FLOAT_BITS,
)
from nptyping.types._object import Object
from nptyping.types._subarray_type import SubArrayType, is_subarray_type
from nptyping.types._structured_type import StructuredType, is_structured_type
from nptyping.types._timedelta64 import Timedelta64
from nptyping.types._unicode import Unicode


def get_type(obj: Any) -> Type['NPType']:
    """
    Return the nptyping type of the given obj. The given obj can be a numpy
    ndarray, a dtype or a Python type. If no corresponding nptyping type
    can be determined, a TypeError is raised.
    :param obj: the object for which an nptyping type is to be returned.
    :return: a subclass of NPType.
    """
    return ClsFunction(_delegates)(obj)


def _get_type_type(type_: type) -> Type['NPType']:
    # Return the nptyping type of a type.
    for super_type, delegate in _delegates:
        if issubclass(type_, super_type):
            break
    return delegate(type_)


def _get_type_dtype(dtype: numpy.dtype) -> Type['NPType']:
    # Return the nptyping type of a numpy dtype.
    if is_subarray_type(dtype):
        return get_subarray_type(dtype)
    if is_structured_type(dtype):
        return get_structured_type(dtype)
    np_type_per_py_type = {
        type: _get_type_type,
        bool: get_type_bool,
        int: get_type_int,
        float: get_type_float,
        str: get_type_str,
        complex: get_type_complex,
        datetime: get_type_datetime64,
        timedelta: get_type_timedelta64,
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
        bits_per_type: Dict[type, int]) -> Type[Number]:
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
def get_type_bool(_: Any) -> Type[Bool]:
    """
    Return the NPType that corresponds to obj.
    :param _: a bool compatible object.
    :return: a Bool type.
    """
    return Bool


# Library private.
def get_type_str(obj: Any) -> Type[Unicode]:
    """
    Return the NPType that corresponds to obj.
    :param obj: a string compatible object.
    :return: a Unicode type.
    """
    if isinstance(obj, numpy.dtype):
        return Unicode[obj.itemsize / 4]
    if obj == str:
        return Unicode
    if not isinstance(obj, str):
        raise TypeError('Unsupported type {}'.format(type(obj)))
    return Unicode[len(obj)]


# Library private.
def get_type_int(obj: Any) -> Type[Int]:
    """
    Return the NPType that corresponds to obj.
    :param obj: an int compatible object.
    :return: a Int type.
    """
    return _get_type_of_number(Int, obj, {
        numpy.int8: 8,
        numpy.int16: 16,
        numpy.int32: 32,
        numpy.int64: 64,
        int: DEFAULT_INT_BITS,
    })


# Library private.
def get_type_uint(obj: Any) -> Type[UInt]:
    """
    Return the NPType that corresponds to obj.
    :param obj: an uint compatible object.
    :return: an UInt type.
    """
    return _get_type_of_number(UInt, obj, {
        numpy.uint8: 8,
        numpy.uint16: 16,
        numpy.uint32: 32,
        numpy.uint64: 64,
        int: DEFAULT_INT_BITS,
    })


# Library private.
def get_type_float(obj: Any) -> Type[Float]:
    """
    Return the NPType that corresponds to obj.
    :param obj: a float compatible object.
    :return: a Float type.
    """
    return _get_type_of_number(Float, obj, {
        numpy.float16: 16,
        numpy.float32: 32,
        numpy.float64: 64,
        float: DEFAULT_FLOAT_BITS,
    })


# Library private.
def get_type_datetime64(_: Any) -> Type[Datetime64]:
    """
    Return the NPType that corresponds to obj.
    :param _: a datetime compatible object.
    :return: a Datetime64 type.
    """
    return Datetime64


# Library private.
def get_type_timedelta64(_: Any) -> Type[Timedelta64]:
    """
    Return the NPType that corresponds to obj.
    :param _: a timedelta compatible object.
    :return: a Timedelta64 type.
    """
    return Timedelta64


# Library private.
def get_type_complex(_: Any) -> Type[Complex128]:
    """
    Return the NPType that corresponds to obj.
    :param _: a complex128 compatible object.
    :return: a Complex128 type.
    """
    return Complex128


# Library private.
def get_structured_type(dtype: numpy.dtype) -> Type[StructuredType]:
    """
    Return the NPType that corresponds to dtype of a structured array.
    :param dtype: a dtype of a structured NumPy array
    :return: a StructuredType type.
    """
    return StructuredType[dtype]


# Library private.
def get_subarray_type(dtype: numpy.dtype) -> Type[SubArrayType]:
    """
    Return the NPType that corresponds to dtype of a subarray.
    :param dtype: a dtype of a NumPy subarray
    :return: a SubArrayType type.
    """
    return SubArrayType[dtype]


_delegates = [
    (NPType, lambda x: x),
    (type, _get_type_type),
    (bool, get_type_bool),
    (int, get_type_int),
    (float, get_type_float),
    (str, get_type_str),
    (complex, get_type_complex),
    (datetime, get_type_datetime64),
    (timedelta, get_type_timedelta64),
    (numpy.datetime64, get_type_datetime64),
    (numpy.timedelta64, get_type_timedelta64),
    (numpy.signedinteger, get_type_int),
    (numpy.unsignedinteger, get_type_uint),
    (numpy.floating, get_type_float),
    (numpy.bool_, get_type_bool),
    (numpy.dtype, _get_type_dtype),
    (numpy.ndarray, _get_type_arrary),
    (object, lambda _: Object),
]
