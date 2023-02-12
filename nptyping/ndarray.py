"""
MIT License

Copyright (c) 2023 Ramon Hagenaars

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import inspect
from abc import ABC
from typing import Any, Tuple

import numpy as np

from nptyping.base_meta_classes import (
    FinalMeta,
    ImmutableMeta,
    InconstructableMeta,
    MaybeCheckableMeta,
    PrintableMeta,
    SubscriptableMeta,
)
from nptyping.error import InvalidArgumentsError
from nptyping.nptyping_type import NPTypingType
from nptyping.shape import Shape
from nptyping.shape_expression import check_shape
from nptyping.structure import Structure
from nptyping.structure_expression import check_structure, check_type_names
from nptyping.typing_ import (
    DType,
    dtype_per_name,
    name_per_dtype,
)


class NDArrayMeta(
    SubscriptableMeta,
    InconstructableMeta,
    ImmutableMeta,
    FinalMeta,
    MaybeCheckableMeta,
    PrintableMeta,
    implementation="NDArray",
):
    """
    Metaclass that is coupled to nptyping.NDArray. It contains all actual logic
    such as instance checking.
    """

    __args__: Tuple[Shape, DType]
    _parameterized: bool

    @property
    def __module__(cls) -> str:
        return cls._get_module(inspect.stack(), "nptyping.ndarray")

    def _get_item(cls, item: Any) -> Tuple[Any, ...]:
        cls._check_item(item)
        shape, dtype = cls._get_from_tuple(item)
        return shape, dtype

    def __instancecheck__(  # pylint: disable=bad-mcs-method-argument
        self, instance: Any
    ) -> bool:
        shape, dtype = self.__args__
        dtype_is_structure = issubclass(dtype, Structure)
        structure_is_ok = dtype_is_structure and check_structure(
            instance.dtype, dtype, dtype_per_name
        )
        return (
            isinstance(instance, np.ndarray)
            and (shape is Any or check_shape(instance.shape, shape))
            and (
                dtype is Any
                or structure_is_ok
                or issubclass(instance.dtype.type, dtype)
            )
        )

    def __str__(cls) -> str:
        shape, dtype = cls.__args__
        return (
            f"{cls.__name__}[{cls._shape_expression_to_str(shape)}, "
            f"{cls._dtype_to_str(dtype)}]"
        )

    def _is_literal_like(cls, item: Any) -> bool:
        # item is a Literal or "Literal enough" (ducktyping).
        return hasattr(item, "__args__")

    def _check_item(cls, item: Any) -> None:
        # Check if the item is what we expect and raise if it is not.
        if not isinstance(item, tuple):
            raise InvalidArgumentsError(f"Unexpected argument of type {type(item)}.")
        if len(item) > 2:
            raise InvalidArgumentsError(f"Unexpected argument {item[2]}.")

    def _get_from_tuple(cls, item: Tuple[Any, ...]) -> Tuple[Shape, DType]:
        # Return the Shape Expression and DType from a tuple.
        shape = cls._get_shape(item[0])
        dtype = cls._get_dtype(item[1])
        return shape, dtype

    def _get_shape(cls, dtype_candidate: Any) -> Shape:
        if dtype_candidate is Any or dtype_candidate is Shape:
            shape = Any
        elif issubclass(dtype_candidate, Shape):
            shape = dtype_candidate
        elif cls._is_literal_like(dtype_candidate):
            shape_expression = dtype_candidate.__args__[0]
            shape = Shape[shape_expression]
        else:
            raise InvalidArgumentsError(
                f"Unexpected argument '{dtype_candidate}', expecting"
                " Shape[<ShapeExpression>]"
                " or Literal[<ShapeExpression>]"
                " or typing.Any."
            )
        return shape

    def _get_dtype(cls, dtype_candidate: Any) -> DType:
        is_dtype = isinstance(dtype_candidate, type) and issubclass(
            dtype_candidate, np.generic
        )
        if dtype_candidate is Any:
            dtype = Any
        elif is_dtype:
            dtype = dtype_candidate
        elif issubclass(dtype_candidate, Structure):
            dtype = dtype_candidate
            check_type_names(dtype, dtype_per_name)
        elif cls._is_literal_like(dtype_candidate):
            structure_expression = dtype_candidate.__args__[0]
            dtype = Structure[structure_expression]
            check_type_names(dtype, dtype_per_name)
        else:
            raise InvalidArgumentsError(
                f"Unexpected argument '{dtype_candidate}', expecting"
                " Structure[<StructureExpression>]"
                " or Literal[<StructureExpression>]"
                " or a dtype"
                " or typing.Any."
            )
        return dtype

    def _dtype_to_str(cls, dtype: Any) -> str:
        if dtype is Any:
            result = "Any"
        elif issubclass(dtype, Structure):
            result = str(dtype)
        else:
            result = name_per_dtype[dtype]
        return result

    def _shape_expression_to_str(cls, shape_expression: Any) -> str:
        return "Any" if shape_expression is Any else str(shape_expression)


class NDArray(NPTypingType, ABC, metaclass=NDArrayMeta):
    """
    An nptyping equivalent of numpy ndarray.

    ## No arguments means an NDArray with any DType and any shape.
    >>> NDArray
    NDArray[Any, Any]

    ## You can provide a DType and a Shape Expression.
    >>> from nptyping import Int32, Shape
    >>> NDArray[Shape["2, 2"], Int32]
    NDArray[Shape['2, 2'], Int32]

    ## Instance checking can be done and the shape is also checked.
    >>> import numpy as np
    >>> isinstance(np.array([[1, 2], [3, 4]]), NDArray[Shape['2, 2'], Int32])
    True
    >>> isinstance(np.array([[1, 2], [3, 4], [5, 6]]), NDArray[Shape['2, 2'], Int32])
    False

    """

    __args__ = (Any, Any)
