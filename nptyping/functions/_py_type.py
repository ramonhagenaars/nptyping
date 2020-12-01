from datetime import datetime, timedelta
from typing import Union, Any

import numpy as np
from typish import ClsFunction, Literal


def py_type(np_type: Union[np.dtype, type, Literal[Any]]) -> type:
    """
    Return the Python equivalent type of a numpy type. Throw a KeyError if no
    match is found for the given type. If the given np_type is not a type, it
    is attempted to create a numpy.dtype for it. Any error that is raised
    during this, is also raised by this function.

    Example:

    >>> py_type(np.int32)
    <class 'int'>

    :param np_type: a numpy type (dtype).
    :return: a Python builtin type.
    """
    np_type = (np.dtype(np_type) if not isinstance(np_type, np.dtype)
               else np_type)
    function = ClsFunction({
        np.dtype: lambda x: _TYPE_PER_KIND[x.kind],
        type: lambda x: py_type(np.dtype(x)),
    })
    return function(np_type)


_TYPE_PER_KIND = {
    'i': int,
    'u': int,
    'f': float,
    'U': str,
    'O': object,
    'b': bool,
    'M': datetime,
    'm': timedelta,
    'c': complex,
}
