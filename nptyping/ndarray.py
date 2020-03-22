from typing import Any, Tuple, Union

import numpy as np
from typish import SubscriptableType, Ellipsis_, ClsDict, Literal

_Size = Union[int, Literal[Any]]  # TODO add type vars as well
_Type = Union[type, np.dtype]


class _NDArrayMeta(SubscriptableType):
    _shape = ...  # Overridden by _NDArray._shape.
    _type = ...  # Overridden by _NDArray._type.

    @property
    def dtype(self):
        return np.dtype(self._type)

    @property
    def shape(self):
        return self._shape

    def __instancecheck__(self, instance):
        return self._is_shape_eq(instance) and self._is_type_eq(instance)

    def _is_shape_eq(cls, instance: np.ndarray) -> bool:

        def _is_eq_to(a: Any, b: Any) -> bool:
            return b is Any or a == b

        if cls._shape is Any:
            return True
        if len(cls._shape) == 2 and cls._shape[1] is ...:
            size = cls._shape[0]
            return all([s == size for s in instance.shape])
        if len(instance.shape) != len(cls._shape):
            return False
        zipped = zip(instance.shape, cls._shape)
        return all([_is_eq_to(a, b) for a, b in zipped])

    def _is_type_eq(cls, instance: np.ndarray) -> bool:
        if cls._type is Any:
            return True
        return cls.dtype == instance.dtype


class _NDArray(metaclass=_NDArrayMeta):
    _shape = Any
    _type = Any

    @classmethod
    def _after_subscription(cls, item: Any) -> None:
        method_per_type = ClsDict({
            _Size: cls._only_size,
            _Type: cls._only_type,
            Tuple[_Size, _Type]: cls._size_and_type,
            Tuple[_Size, ...]: cls._only_sizes,
            Tuple[Tuple[_Size, ...], _Type]: cls._sizes_and_type,
            Tuple[Tuple[_Size, Ellipsis_], _Type]: cls._sizes_and_type,
        })
        method = method_per_type.get(item)
        if not method:
            raise TypeError('Invalid parameter for NDArray: "{}"'.format(item))
        return method(item)

    @classmethod
    def _only_size(cls, item: int):
        # E.g. NDArray[3]
        # The given item is the size of the single dimension.
        cls._shape = (item,)

    @classmethod
    def _only_type(cls, item: type):
        # E.g. NDArray[int]
        # The given item is the type of the single dimension.
        cls._type = item

    @classmethod
    def _size_and_type(cls, item: Tuple[_Size, _Type]):
        # E.g. NDArray[3, int]
        # The given item is the size of the single dimension and its type.
        cls._shape = (item[0],)
        cls._type = item[1]

    @classmethod
    def _only_sizes(cls, item: Tuple[_Size, ...]):
        # E.g. NDArray[(2, Any, 2)]
        # The given item is a tuple with just sizes of the dimensions.
        cls._shape = item

    @classmethod
    def _sizes_and_type(cls, item: Tuple[Tuple[_Size, ...], _Type]):
        # E.g. NDArray[(2, Any, 2), int]
        # The given item is a tuple with sizes of the dimensions and the type.
        # Or e.g. NDArray[(3, ...), int]
        # The given item is a tuple with sizes of n dimensions and the type.
        cls._only_sizes(item[0])
        cls._only_type(item[1])


class NDArray(np.ndarray, _NDArray):
    ...
