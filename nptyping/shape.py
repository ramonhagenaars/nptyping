"""
MIT License

Copyright (c) 2022 Ramon Hagenaars

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
from typing import (
    Any,
    Dict,
    Set,
    Tuple,
)

from nptyping.error import InvalidArgumentsError
from nptyping.shape_expression import (
    get_dimensions,
    normalize_shape_expression,
    remove_labels,
    validate_shape_expression,
)
from nptyping.subscriptable_meta import SubscriptableMeta


class ShapeMeta(SubscriptableMeta, cls_name="Shape"):
    """
    Metaclass that is coupled to nptyping.Shape. It contains all actual logic
    such as instance checking.
    """

    _known_expressions: Set[str] = set()

    def _get_item(cls, item: Any) -> Tuple[Any, ...]:
        if not isinstance(item, str):
            raise InvalidArgumentsError(
                f"Unexpected argument of type" f" {type(item)}, expecting a string."
            )

        if item in cls._known_expressions:
            # No need to do costly validations and normalizations if it has been done
            # before.
            return (item,)

        validate_shape_expression(item)
        norm_shape_expression = normalize_shape_expression(item)
        cls._known_expressions.add(norm_shape_expression)
        return (norm_shape_expression,)

    def _get_additional_values(cls, item: Any) -> Dict[str, Any]:
        dim_strings = get_dimensions(item)
        dim_string_without_labels = remove_labels(dim_strings)
        return {"prepared_args": dim_string_without_labels}

    def __subclasscheck__(cls, subclass: Any) -> bool:
        return type(  # pylint: disable=unidiomatic-typecheck
            subclass
        ) is ShapeMeta and (subclass.__args__ == cls.__args__ or not cls._parameterized)

    def __eq__(cls, other: Any) -> bool:
        return hasattr(other, "__args__") and other.__args__ == cls.__args__

    def __hash__(cls) -> int:
        return hash(cls.__args__)

    def __str__(cls: "Shape") -> str:
        return f"Shape['{cls.__args__[0]}']"

    def __repr__(cls) -> str:
        return str(cls)


class Shape(metaclass=ShapeMeta):
    """
    A container for shape expressions that describe the shape of an multi
    dimensional array.

    Simple example:

    >>> Shape['2, 2']
    Shape['2, 2']

    A Shape can be compared to a typing.Literal. You can use Literals in
    NDArray as well.

    >>> from typing import Literal

    >>> Shape['2, 2'] == Literal['2, 2']
    True

    """

    __args__ = ("*, ...",)
    prepared_args = "*, ..."
