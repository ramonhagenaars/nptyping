"""
The nptyping module: support for typing Numpy datatypes.
"""
from functools import lru_cache
import numpy as np


def _meta(generic_type: type = None, rows: int = ..., cols: int = ...) -> type:
    class _ArrayMeta(type):
        _generic_type = generic_type
        _rows = rows
        _cols = cols

        @lru_cache(maxsize=32)
        def __getitem__(cls, item: object) -> type:
            generic_type = item
            rows = ...
            cols = ...
            if isinstance(item, tuple):
                if not len(item):
                    raise TypeError('Parameter Array[...] cannot be empty')

                generic_type = tuple()
                for index, value in enumerate(item):
                    if isinstance(value, type):
                        generic_type += (value,)
                    else:
                        break
                else:
                    index += 1

                if len(generic_type) == 1:
                    generic_type = generic_type[0]

                rowcol_types = [int, type(...), type(None)]
                if len(item) > index:
                    if type(item[index]) not in rowcol_types:
                        raise TypeError('Unexpected type %s, expecting int or ... or None' % item[index])
                    rows = item[index] or ...
                index += 1
                if len(item) > index:
                    if isinstance(generic_type, tuple):
                        raise TypeError('You are not allowed to specify a column count, combined with multiple column '
                                        'types.')
                    if type(item[index]) not in rowcol_types:
                        raise TypeError('Unexpected type %s, expecting int or ... or None' % item[index])
                    cols = item[index] or ...

            class _Array(metaclass=_meta(generic_type, rows, cols)):
                pass

            result = type('Array', (_Array,), {})
            return result

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
                    if isinstance(cls._generic_type, tuple):
                        inst_dtypes = [inst.dtype[name] for name in inst.dtype.names]
                        cls_dtypes = [np.dtype(typ) for typ in cls._generic_type]
                        result = inst_dtypes == cls_dtypes
                    else:
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
