from typing import Any, Tuple, Union

import numpy as np
from typish import SubscriptableType, Ellipsis_, instance_of, ClsDict

_Size = Union[int, Ellipsis_]  # TODO add type vars as well
_Type = Union[type, np.dtype]


def _is_eq_to(a: Any, b: Any) -> bool:
    return b is Any or a == b


class _NDArrayMeta(SubscriptableType):

    def __instancecheck__(self, instance):
        return self._is_shape_eq(instance) and self._is_type_eq(instance)

    def _is_shape_eq(cls, instance: np.ndarray) -> bool:
        if cls.shape is Any:
            return True
        if len(instance.shape) != len(cls.shape):
            return False
        zipped = zip(instance.shape, cls.shape)
        return all([_is_eq_to(a, b) for a, b in zipped])

    def _is_type_eq(cls, instance: np.ndarray) -> bool:
        if cls.type_ is Any:
            return True
        return cls.dtype(cls) == instance.dtype


class _NDArray(metaclass=_NDArrayMeta):
    shape = Any
    type_ = Any

    def dtype(self):
        return np.dtype(self.type_)

    @classmethod
    def _after_subscription(cls, item: Any) -> None:
        method_per_type = ClsDict({
            int: cls._only_size,
            Ellipsis_: cls._only_ellipsis,
            _Type: cls._only_type,
            Tuple[_Size, _Type]: cls._size_and_type,
            Tuple[_Size, ...]: cls._only_sizes,
            Tuple[Tuple[_Size, ...], _Type]: cls._sizes_and_type,
        })
        method = method_per_type.get(item)
        if not method:
            raise TypeError('Invalid parameter for NDArray: "{}"'.format(item))
        return method(item)

    @classmethod
    def _only_ellipsis(cls, _: Ellipsis_):
        # I.e. NDArray[...]
        # The given item is an ellipsis; a single dimension of any size of any
        # type.
        cls.shape = (Any,)

    @classmethod
    def _only_size(cls, item: int):
        # E.g. NDArray[3]
        # The given item is the size of the single dimension.
        cls.shape = (item,)

    @classmethod
    def _only_type(cls, item: type):
        # E.g. NDArray[int]
        # The given item is the type of the single dimension.
        cls.type_ = item

    @classmethod
    def _size_and_type(cls, item: Tuple[_Size, _Type]):
        # E.g. NDArray[3, int]
        # The given item is the size of the single dimension and its type.
        cls.shape = (item[0],)
        cls.type_ = item[1]

    @classmethod
    def _only_sizes(cls, item: Tuple[_Size, ...]):
        # E.g. NDArray[(2, ..., 2)]
        # The given item is a tuple with just sizes of the dimensions.
        cls.shape = tuple()
        for d in item:
            size = d
            if instance_of(d, Ellipsis_):
                size = Any
            cls.shape += (size,)

    @classmethod
    def _sizes_and_type(cls, item: Tuple[Tuple[_Size, ...], _Type]):
        # E.g. NDArray[(2, ..., 2), int]
        # The given item is a tuple with sizes of the dimensions and the type.
        cls._only_sizes(item[0])
        cls._only_type(item[1])


class NDArray(_NDArray):
    ...
