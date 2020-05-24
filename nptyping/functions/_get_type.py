from typing import Any, Type

import numpy
from typish import ClsFunction

from nptyping.functions._py_type import py_type
from nptyping.types._nptype import NPType
from nptyping.types._number import Int, Float, UInt
from nptyping.types.ndarray import NDArray


def get_type(obj: Any) -> Type[NPType]:
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
        (numpy.dtype, _get_type_dtype),
        (numpy.ndarray, _get_type_arrary),
        (numpy.signedinteger, Int.type_of),
        (numpy.unsignedinteger, UInt.type_of),
        (numpy.floating, Float.type_of),
    ])

    if not function.understands(obj):
        raise TypeError('Type "{}" not understood.'.format(type(obj).__name__))

    return function(obj)


def _get_type_type(type_: type) -> Type[NPType]:
    # Return the nptyping type of a type.
    if issubclass(type_, numpy.signedinteger):
        return Int.type_of(type_)
    if issubclass(type_, numpy.unsignedinteger):
        return UInt.type_of(type_)
    if issubclass(type_, numpy.floating):
        return Float.type_of(type_)
    raise TypeError('Type "{}" not understood.'.format(type_.__name__))


def _get_type_dtype(dtype: numpy.dtype) -> Type[NPType]:
    # Return the nptyping type of a numpy dtype.
    np_type_per_py_type = {
        int: Int,
        float: Float,
    }
    bits = dtype.itemsize * 8
    cls = np_type_per_py_type[(py_type(dtype))]
    return cls[bits]


def _get_type_arrary(arr: numpy.ndarray) -> Type[NPType]:
    # Return the nptyping type of a numpy array.
    type_ = get_type(arr.dtype)
    return NDArray[arr.shape, type_]
