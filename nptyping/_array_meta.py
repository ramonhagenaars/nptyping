"""
PRIVATE MODULE: do not import (from) it directly.
This module contains meta functionality for the ``Array`` type.
"""
from functools import lru_cache
from typing import Type
import numpy as np


class ArrayMeta(type):
    _generic_type = None
    _rows = None
    _cols = None

    @lru_cache(maxsize=32)
    def __getitem__(cls, item: object) -> Type['Array']:
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

        class _Array(metaclass=meta(generic_type, rows, cols)):
            def func(self): pass
            pass

        result = type('Array', (_Array,), {})
        return result

    @classmethod
    def __instancecheck__(mcs, inst):
        result = False
        if isinstance(inst, np.ndarray):
            result = True  # In case of an empty array or no _generic_type.
            rows = 0
            cols = 0
            if len(inst.shape) > 0:
                rows = inst.shape[0]
            if len(inst.shape) > 1:
                cols = inst.shape[1]

            if inst.size > 0 and mcs._generic_type:
                if isinstance(mcs._generic_type, tuple):
                    inst_dtypes = [inst.dtype[name] for name in inst.dtype.names]
                    cls_dtypes = [np.dtype(typ) for typ in mcs._generic_type]
                    result = inst_dtypes == cls_dtypes
                else:
                    result = isinstance(inst[0], mcs._generic_type)
                    result |= inst.dtype == np.dtype(mcs._generic_type)
                result &= mcs._rows is ... or mcs._rows == rows
                result &= mcs._cols is ... or mcs._cols == cols
        return result


def meta(generic_type: type = None, rows: int = ..., cols: int = ...) -> ArrayMeta:
    # Create a meta class with the given arguments.
    _metaclass = type('_ArrayMeta', (ArrayMeta,), {})
    _metaclass._generic_type = generic_type
    _metaclass._rows = rows
    _metaclass._cols = cols
    return _metaclass
