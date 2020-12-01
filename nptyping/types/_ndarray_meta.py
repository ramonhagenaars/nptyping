from collections import OrderedDict
from typing import Any, Tuple, Union

import numpy as np
from typish import SubscriptableType, Literal, ClsFunction, EllipsisType

from nptyping.types._nptype import NPType

_Size = Union[int, Literal[Any]]  # TODO add type vars as well
_Type = Union[type, Literal[Any], np.dtype]
_NSizes = Tuple[_Size, EllipsisType]
_SizeAndType = Tuple[_Size, _Type]
_Sizes = Tuple[_Size, ...]
_SizesAndType = Tuple[Tuple[_Size, ...], _Type]
_NSizesAndType = Tuple[_NSizes, _Type]
_Default = Tuple[Tuple[Literal[Any], EllipsisType], Literal[Any]]

# The types below are for Python 3.5 compatibility. Union[Literal[Any], type]
# is translated to Union[type], because of Literal inheriting from type.
_SizeAndTypeAny = Tuple[_Size, Literal[Any]]
_SizesAndTypeAny = Tuple[Tuple[_Size, ...], Literal[Any]]
_NSizesAndTypeAny = Tuple[_NSizes, Literal[Any]]


def _is_eq_to(this: Any, that: Any) -> bool:
    return that is Any or this == that


class _NDArrayMeta(SubscriptableType):
    _shape = tuple()  # type: Union[Tuple[int, ...], Tuple[int, EllipsisType]]
    _type = ...  # type: Union[type, Literal[Any]]

    @property
    def shape(cls) -> Tuple[int, ...]:
        """
        Return the shape as a tuple of ints.
        :return: the shape as a tuple of ints.
        """
        return cls._shape

    def __repr__(cls) -> str:
        shape_ = cls._shape
        if len(cls._shape) == 2 and cls._shape[1] is ...:
            shape_ = (cls._shape[0], '...')

        return 'NDArray[{}, {}]'.format(shape_, cls._type).replace('\'', '')

    def __str__(cls) -> str:
        return repr(cls)

    def __eq__(cls, other: object) -> bool:
        return (isinstance(other, _NDArrayMeta)
                and cls._shape == other._shape
                and _is_eq_to(cls._type, other._type))

    def __instancecheck__(cls, instance: Any) -> bool:
        """
        Check whether the given instance conforms the current NDArray type by
        checking the shape and the dtype.
        :param instance: the instance that is checked.
        :return: True if instance is an instance of cls.
        """
        return _NDArrayMeta.__subclasscheck__(
            cls, _NDArray[instance.shape, instance.dtype])

    def __subclasscheck__(cls, subclass: type) -> bool:
        """
        Check whether the given class is a sub class of cls.
        :param subclass: the class that is to be checked.
        :return: True if subclass is a sub class of cls.
        """
        return (subclass == cls
                or (isinstance(subclass, _NDArrayMeta)
                    and cls._is_dtype_eq(subclass._type)  # pylint: disable=no-value-for-parameter # noqa
                    and cls._is_shape_eq(subclass.shape)))  # pylint: disable=no-value-for-parameter # noqa

    def __hash__(cls) -> int:
        """
        Hash this _NDArrayMeta by means of its attributes.
        :return: a hash (int).
        """
        return hash((cls._shape, cls._type))

    def _is_shape_eq(cls, shape: Tuple[int, ...]) -> bool:
        if cls._shape == (Any, ...):
            return True
        if len(cls._shape) == 2 and cls._shape[1] is ...:
            size = cls._shape[0]
            return all([s == size for s in shape])
        if len(shape) != len(cls._shape):
            return False
        zipped = zip(shape, cls._shape)
        return all([_is_eq_to(a, b) for a, b in zipped])

    def _is_dtype_eq(cls, nptype: NPType) -> bool:
        return cls._type is Any or issubclass(nptype, cls._type)


class _NDArray(NPType, metaclass=_NDArrayMeta):
    _shape = (Any, ...)  # type: Union[Tuple[int, ...], Tuple[Any, EllipsisType]]  # noqa
    _type = Any
    _special = True  # Added to be able to compile types with sphinx.

    @classmethod
    def _after_subscription(cls, item: Any) -> None:
        method = ClsFunction(OrderedDict([
            (_Size, cls._only_size),
            (_Type, cls._only_type),
            (_NSizes, lambda _: ...),
            (_SizeAndType, cls._size_and_type),
            (_SizeAndTypeAny, cls._size_and_type),  # For Python 3.5.
            (_Sizes, cls._only_sizes),
            (_SizesAndType, cls._sizes_and_type),
            (_SizesAndTypeAny, cls._sizes_and_type),  # For Python 3.5.
            (_NSizesAndType, cls._sizes_and_type),
            (_NSizesAndTypeAny, cls._sizes_and_type),  # For Python 3.5.
            (_Default, lambda _: ...),
        ]))

        if not method.understands(item):
            raise TypeError('Invalid parameter for NDArray: "{}"'.format(item))
        method(item)

    @classmethod
    def _only_size(cls, item: int) -> None:
        # E.g. NDArray[3]
        # The given item is the size of the single dimension.
        cls._shape = (item,)

    @classmethod
    def _only_type(cls, item: type) -> None:
        # E.g. NDArray[int]
        # The given item is the type of the single dimension.
        from nptyping import get_type  # Put here to prevent cyclic import.
        cls._type = Any if item is Any else get_type(item)

    @classmethod
    def _size_and_type(cls, item: Tuple[_Size, _Type]) -> None:
        # E.g. NDArray[3, int]
        # The given item is the size of the single dimension and its type.
        cls._shape = (item[0],)
        cls._only_type(item[1])

    @classmethod
    def _only_sizes(cls, item: Tuple[_Size, ...]) -> None:
        # E.g. NDArray[(2, Any, 2)]
        # The given item is a tuple with just sizes of the dimensions.
        cls._shape = item

    @classmethod
    def _sizes_and_type(cls, item: Tuple[Tuple[_Size, ...], _Type]) -> None:
        # E.g. NDArray[(2, Any, 2), int]
        # The given item is a tuple with sizes of the dimensions and the type.
        # Or e.g. NDArray[(3, ...), int]
        # The given item is a tuple with sizes of n dimensions and the type.
        cls._only_sizes(item[0])
        cls._only_type(item[1])
