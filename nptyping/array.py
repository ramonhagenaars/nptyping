# pylint: skip-file
"""
The array module: support for typing Numpy ndarrays.
"""
import warnings

import numpy as np

from nptyping._array_meta import _Array

warnings.warn("The use of nptyping.Array is deprecated in favor of "
              "nptyping.NDArray", DeprecationWarning)


class Array(_Array, np.ndarray):
    """
    A representation of the `numpy.ndarray`.

    Example of an array with an undefined generic type and shape:
        `Array`

    Example of an array with a defined generic type:
        `Array[int]`

    Example of an array with a defined generic type and shape (rows):
        `Array[int, 3]`
        `Array[int, 3, ...]`
        `Array[int, 3, None]`

    Examples of an array with a defined generic type and shape (cols):
        `Array[int, None, 2]`
        `Array[int, ..., 2]`

    Example of an array with a defined generic type and shape (rows and cols):
        `Array[int, 3, 2]`

    """
