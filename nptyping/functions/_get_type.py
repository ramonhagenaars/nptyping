from typing import Any, Type

import numpy
from typish import ClsFunction

from nptyping.functions._np_type import np_type
from nptyping.functions._py_type import py_type
from nptyping.types._nptype import NPType
from nptyping.types._number import Int, Float
from nptyping.types.ndarray import NDArray


def get_type(obj: Any) -> Type[NPType]:
    if isinstance(obj, type):
        if issubclass(obj, numpy.signedinteger):
            function = Int.type_of
    else:
        function = ClsFunction([
            (int, Int.type_of),
            (float, Float.type_of),
            (numpy.dtype, _get_type_dtype),
            (numpy.ndarray, _get_type_arrary),
            (numpy.signedinteger, Int.type_of),
        ])
    return function(obj)


def _get_type_dtype(dtype: numpy.dtype) -> Type[NPType]:
    bits = dtype.itemsize * 8
    cls = np_type(py_type(dtype))
    return cls[bits]


def _get_type_arrary(arr: numpy.ndarray):
    type_ = get_type(arr.dtype)
    return NDArray[arr.shape, type_]
