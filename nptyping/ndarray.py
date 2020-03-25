import numpy as np

from nptyping._ndarray_meta import _NDArray


class NDArray(np.ndarray, _NDArray):
    """
    NDArray is a representation of numpy.ndarray.

    An Array with any dimensions of any size and any type:
    >>> NDArray
    NDArray[(typing.Any, ...), typing.Any]

    An array with 1 dimension of any size and any type:
    >>> from typing import Any
    >>> NDArray[Any]
    NDArray[(typing.Any,), typing.Any]

    An array with 1 dimension of size 3 and any type:
    >>> NDArray[3]
    NDArray[(3,), typing.Any]

    An array with any dimensions of any size and type int:
    >>> NDArray[int]
    NDArray[(typing.Any, ...), int]

    An array with 1 dimension of size 3 and type int:
    >>> NDArray[3, int]
    NDArray[(3,), int]

    An array with any dimensions of size 3 and type int:
    >>> NDArray[(3, ...), int]
    NDArray[(3, ...), int]

    An array with 3 dimensions of sizes 3, 3, 5 and type int:
    >>> NDArray[(3, 3, 5), int]
    NDArray[(3, 3, 5), int]

    """
