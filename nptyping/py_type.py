from typing import Union

import numpy as np
from typish import ClsFunction


def py_type(np_type: Union[np.dtype, type]) -> type:
    """
    Return the Python equivalent type of a numpy type. Throw a KeyError if no
    match is found for the given type.

    Example:

    >>> py_type(np.int32)
    <class 'int'>

    :param np_type: a numpy type (dtype).
    :return: a Python builtin type.
    """
    function = ClsFunction({
        np.dtype: lambda x: _TYPE_PER_KIND[x.kind],
        type: lambda x: py_type(np.dtype(x)),
    })
    return function(np_type)


_TYPE_PER_KIND = {
    'i': int,
    'f': float,
    'U': str,
    'O': object,
}
