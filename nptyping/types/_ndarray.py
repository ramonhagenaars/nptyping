from typing import Type

import numpy as np

from nptyping.types._ndarray_meta import _NDArray


class NDArray(_NDArray, np.ndarray):
    """
    NDArray is a representation of numpy.ndarray.

    An Array with any dimensions of any size and any type:
    >>> NDArray
    NDArray[(typing.Any, ...), typing.Any]

    An array with 1 dimension of any size and any type:
    >>> from typing import Any
    >>> from nptyping import Int64
    >>> NDArray[Any]
    NDArray[(typing.Any,), typing.Any]

    An array with 1 dimension of size 3 and any type:
    >>> NDArray[3]
    NDArray[(3,), typing.Any]

    An array with any dimensions of any size and type int:
    >>> NDArray[Int64]
    NDArray[(typing.Any, ...), Int[64]]

    An array with 1 dimension of size 3 and type int:
    >>> NDArray[3, Int64]
    NDArray[(3,), Int[64]]

    An array with any dimensions of size 3 and type int:
    >>> NDArray[(3, ...), Int64]
    NDArray[(3, ...), Int[64]]

    An array with 3 dimensions of sizes 3, 3, 5 and type int:
    >>> NDArray[(3, 3, 5), Int64]
    NDArray[(3, 3, 5), Int[64]]

    """

    # These variables are to let typish know to use the custom checks.
    __instancecheck__ = None
    __subclasscheck__ = None

    @staticmethod
    def type_of(arr: np.ndarray) -> Type['NDArray']:
        """
        Return an nptyping.NDArray type T such that isinstance(arr, T).

        >>> NDArray.type_of(np.array([[1, 2], [3, 4.0]]))
        NDArray[(2, 2), Float[64]]

        :param arr: any numpy.ndarray.
        :return: a nptyping.NDArray.
        """
        return NDArray[arr.shape, arr.dtype]
