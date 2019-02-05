"""
The nptyping module: support for typing Numpy datatypes.
"""
import numpy as np


def _meta(generic_type: type = None, rows: int = ..., cols: int = ...) -> type:
    class _ArrayMeta(type):
        _generic_type = generic_type
        _rows = rows
        _cols = cols

        @classmethod
        def __instancecheck__(cls, inst):
            result = False
            if isinstance(inst, np.ndarray):
                result = True  # In case of an empty array or no _generic_type.
                rows = 0
                cols = 0
                if len(inst.shape) > 0:
                    rows = inst.shape[0]
                if len(inst.shape) > 1:
                    cols = inst.shape[1]

                if inst.size > 0 and cls._generic_type:
                    result = isinstance(inst[0], cls._generic_type)
                    result |= inst.dtype == np.dtype(cls._generic_type)
                    result &= cls._rows is ... or cls._rows == rows
                    result &= cls._cols is ... or cls._cols == cols
            return result

    return _ArrayMeta


class Array(metaclass=_meta()):
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
    _instances = {}

    @classmethod
    def __class_getitem__(cls, item: object) -> type:
        if item in Array._instances:
            return Array._instances[item]

        generic_type = item
        rows = ...
        cols = ...
        if isinstance(item, tuple):
            if not len(item):
                raise TypeError('Parameter Array[...] cannot be empty')
            generic_type = item[0]
            if len(item) > 1 and item[1] is not None:
                rows = item[1]
            if len(item) > 2 and item[2] is not None:
                cols = item[2]

        class _Array(metaclass=_meta(generic_type, rows, cols)):
            pass
        result = type('Array', (_Array,), {})
        Array._instances[item] = result
        return result
