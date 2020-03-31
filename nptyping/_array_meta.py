# pylint: skip-file
"""
PRIVATE MODULE: do not import (from) it directly.
This module contains meta functionality for the ``Array`` type.
"""
from functools import lru_cache

import numpy as np
from typish import SubscriptableType
from typish._types import Ellipsis_, NoneType


class _ArrayMeta(SubscriptableType):
    # A Meta class for the Array class.
    @lru_cache()
    def __getitem__(self, item):
        return SubscriptableType.__getitem__(self, item)

    def __instancecheck__(self, inst):
        result = False
        if isinstance(inst, np.ndarray):
            result = True  # In case of an empty array or no _generic_type.
            rows = 0
            cols = 0
            if len(inst.shape) > 0:
                rows = inst.shape[0]
            if len(inst.shape) > 1:
                cols = inst.shape[1]

            if inst.size > 0 and self.generic_type:
                if isinstance(self.generic_type, tuple):
                    inst_dtypes = [inst.dtype[name]
                                   for name in inst.dtype.names]
                    cls_dtypes = [np.dtype(typ) for typ in self.generic_type]
                    result = inst_dtypes == cls_dtypes
                else:
                    result = isinstance(inst[0], self.generic_type)
                    result |= inst.dtype == np.dtype(self.generic_type)
                result &= self.rows is ... or self.rows == rows
                result &= self.cols is ... or self.cols == cols
        return result


class _Array(metaclass=_ArrayMeta):
    # This class exists to keep the Array class as clean as possible.
    __origin__ = 'Array'
    __args__ = tuple()
    _ROWCOL_TYPES = [int, Ellipsis_, NoneType]
    generic_type = None
    rows = ...
    cols = ...

    def __new__(cls, *args, **kwargs):
        raise TypeError("Cannot instantiate abstract class Array")

    @classmethod
    def _after_subscription(cls, item):
        if not isinstance(item, tuple):
            cls.generic_type = item
        else:
            if not len(item):
                raise TypeError('Parameter Array[...] cannot be empty')

            # Collect all elements in item that are types and keep track of
            # the index.
            cls.generic_type = tuple()
            for index, value in enumerate(item):
                if isinstance(value, type):
                    cls.generic_type += (value,)
                else:
                    break
            else:
                index += 1

            # If there is only one type defined before, then store that type
            # rather than a tuple.
            if len(cls.generic_type) == 1:
                cls.generic_type = cls.generic_type[0]

            if len(item) > index:
                if type(item[index]) not in cls._ROWCOL_TYPES:
                    raise TypeError('Unexpected type %s, expecting int or ... '
                                    'or None' % item[index])
                cls.rows = item[index] or ...
            index += 1

            if len(item) > index:
                if isinstance(cls.generic_type, tuple):
                    raise TypeError('You are not allowed to specify a column '
                                    'count, combined with multiple column '
                                    'types.')
                if type(item[index]) not in cls._ROWCOL_TYPES:
                    raise TypeError('Unexpected type %s, expecting int or ... '
                                    'or None' % item[index])
                cls.cols = item[index] or ...
