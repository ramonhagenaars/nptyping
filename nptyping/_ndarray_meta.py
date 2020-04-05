from collections import OrderedDict
from typing import Any, Tuple, Union

import numpy as np
from typish import SubscriptableType, Literal, ClsFunction, EllipsisType

_Size = Union[int, Literal[Any]]  # TODO add type vars as well
_Type = Union[type, Literal[Any], np.dtype]
_NSizes = Tuple[_Size, EllipsisType]
_SizeAndType = Tuple[_Size, _Type]
_Sizes = Tuple[_Size, ...]
_SizesAndType = Tuple[Tuple[_Size, ...], _Type]
_NSizesAndType = Tuple[_NSizes, _Type]
_Default = Tuple[Tuple[Literal[Any], EllipsisType], Literal[Any]]


class _NDArrayMeta(SubscriptableType):
    _shape = tuple()  # Overridden by _NDArray._shape.
    _type = ...  # Overridden by _NDArray._type.

    @property
    def dtype(cls) -> np.dtype:
        """
        Return the numpy dtype.
        :return: the numpy dtype.
        """
        return np.dtype(cls._type)  # TODO if type is Any, this wont work

    @property
    def shape(cls) -> Tuple[int, int]:
        """
        Return the shape as a tuple of ints.
        :return: the shape as a tuple of ints.
        """
        return cls._shape

    def __repr__(cls):
        shape_ = cls._shape
        if len(cls._shape) == 2 and cls._shape[1] is ...:
            shape_ = (cls._shape[0], '...')

        type_ = getattr(cls._type, '__name__', cls._type)
        return 'NDArray[{}, {}]'.format(shape_, type_).replace('\'', '')

    def __str__(cls):
        return repr(cls)

    def __eq__(cls, other) -> bool:
        return (isinstance(other, _NDArrayMeta)
                and cls._shape == other._shape
                and cls._type == other._type)

    def __instancecheck__(cls, instance: np.ndarray) -> bool:
        """
        Checks whether the given instance conforms the current NDArray type by
        checking the shape and the dtype.
        :param instance: a numpy.ndarray.
        :return: True if instance is an instance of cls.
        """
        return (isinstance(instance, np.ndarray)
                and _NDArrayMeta._is_shape_eq(cls, instance)
                and _NDArrayMeta._is_type_eq(cls, instance))

    def __hash__(cls) -> int:
        """
        Hash this _NDArrayMeta by means of its attributes.
        :return: a hash (int).
        """
        return hash((cls._shape, cls._type))

    def _is_shape_eq(cls, instance: np.ndarray) -> bool:

        def _is_eq_to(this: Any, that: Any) -> bool:
            return that is Any or this == that

        if cls._shape == (Any, ...):
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
    _shape = (Any, ...)
    _type = Any

    @classmethod
    def _after_subscription(cls, item: Any) -> None:
        method = ClsFunction(OrderedDict([
            (_Size, cls._only_size),
            (_Type, cls._only_type),
            (_NSizes, lambda _: ...),
            (_SizeAndType, cls._size_and_type),
            (_Sizes, cls._only_sizes),
            (_SizesAndType, cls._sizes_and_type),
            (_NSizesAndType, cls._sizes_and_type),
            (_Default, lambda _: ...),
        ]))

        if not method.understands(item):
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
