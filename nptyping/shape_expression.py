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
import re
import string
from functools import lru_cache
from typing import (
    Any,
    List,
    Tuple,
    Union,
)

from nptyping.error import InvalidShapeError
from nptyping.typing_ import Literal


@lru_cache()
def check_shape(shape, shape_expression):
    """
    Check whether the given shape corresponds to the given shape_expression.
    :param shape: the shape in question.
    :param shape_expression: the shape expression to which shape is tested.
    :return: True if the given shape corresponds to shape_expression.
    """
    dim_strings = _get_dimensions(shape_expression)
    dim_strings = _remove_labels(dim_strings)
    dim_strings = _handle_ellipsis(dim_strings, shape)
    return _check_dimensions_against_shape(dim_strings, shape)


def validate_shape_expression(shape_expression: Union[str, Literal[Any]]) -> None:
    """
    Validate shape_expression and raise an InvalidShapeError if it is not
    considered valid.
    :param shape_expression: the shape expression to validate.
    :return: None.
    """

    if shape_expression is not Any and not re.match(
        _REGEX_SHAPE_EXPRESSION, shape_expression
    ):
        raise InvalidShapeError(f"'{shape_expression}' is not a valid shape expression")


def normalize_shape_expression(
    shape_expression: Union[str, Literal[Any]]
) -> Union[str, Literal[Any]]:
    """
    Normalize the given shape expression, e.g. by removing whitespaces, making
    similar expressions look the same.
    :param shape_expression: the shape expression that is to be normalized.
    :return: a normalized shape expression.
    """
    if shape_expression is Any:
        return Any
    # Replace whitespaces right before labels with $.
    shape_expression = re.sub(rf"\s*{_REGEX_LABEL}", r"$\1", shape_expression)
    # Let all commas be followed by a $.
    shape_expression = shape_expression.replace(",", ",$")
    # Remove all whitespaces left.
    shape_expression = re.sub(r"\s*", "", shape_expression)
    # Remove $ right after a bracket.
    shape_expression = re.sub(r"\[\$+", "[", shape_expression)
    # Replace $ with a single space.
    shape_expression = re.sub(r"\$+", " ", shape_expression)

    if shape_expression == "*, ...":
        return Any
    return shape_expression


def _check_dimensions_against_shape(dimensions: List[str], shape: Tuple[int]) -> bool:
    # Walk through the dimensions and test them against the given shape,
    # taking into consideration variables, wildcards, etc.
    if len(shape) != len(dimensions):
        return False
    assigned_variables = {}
    for inst_dim, cls_dim in zip(shape, dimensions):
        cls_dim_ = cls_dim.strip()
        inst_dim_ = str(inst_dim)
        if _is_variable(cls_dim_):
            # Since cls_dim_ is a variable, try to assign it with
            # inst_dim_. This always succeeds if a variable with the same
            # name hasn't been assigned already.
            if (
                cls_dim_ in assigned_variables
                and assigned_variables[cls_dim_] != inst_dim_
            ):
                result = False
                break
            assigned_variables[cls_dim_] = inst_dim_
        elif inst_dim_ != cls_dim_ and not _is_wildcard(cls_dim_):
            # Identical dimension sizes or wildcards are fine.
            result = False
            break
    else:
        # All is well, no errors have been encountered.
        result = True
    return result


def _is_variable(dim: str) -> bool:
    # Return whether dim is a variable.
    return dim[0] in string.ascii_uppercase


def _is_wildcard(dim: str) -> bool:
    # Return whether dim is a wildcard (i.e. the character that takes any
    # dimension size).
    return dim == "*"


def _get_dimensions(dimension: str) -> List[str]:
    # Find all "break downs" in a shape expressions (the parts between
    # brackets) and replace them with mere dimension sizes.
    dimension_without_breakdowns = dimension
    for dim_breakdown in re.findall(r"(\[.+?\])", dimension_without_breakdowns):
        dim_size = len(dim_breakdown.split(","))
        dimension_without_breakdowns = dimension_without_breakdowns.replace(
            dim_breakdown, str(dim_size)
        )
    return dimension_without_breakdowns.split(",")


def _remove_labels(dimensions: List[str]) -> List[str]:
    # Remove all labels (words that start with a lowercase).
    return [re.sub(r"\b[a-z]\w*", "", dim) for dim in dimensions]


def _handle_ellipsis(dimensions: List[str], shape: Tuple[int]) -> List[str]:
    # Let the ellipsis allows for any number of dimensions by replacing the
    # ellipsis with the dimension size repeated the number of times that
    # corresponds to the shape of the instance.
    result = dimensions
    if len(dimensions) == 2 and dimensions[1].strip() == "...":
        result = dimensions[0] * len(shape)
    return result


_REGEX_SEPARATOR = r"(\s*,\s*)"
_REGEX_DIMENSION_SIZE = r"(\s*[0-9]+\s*)"
_REGEX_VARIABLE = r"(\s*\b[A-Z]\w*\s*)"
_REGEX_LABEL = r"(\s*\b[a-z]\w*\s*)"
_REGEX_LABELS = rf"({_REGEX_LABEL}({_REGEX_SEPARATOR}{_REGEX_LABEL})*)"
_REGEX_WILDCARD = r"(\s*\*\s*)"
_REGEX_DIMENSION_BREAKDOWN = rf"(\s*\[{_REGEX_LABELS}\]\s*)"
_REGEX_DIMENSION = (
    rf"({_REGEX_DIMENSION_SIZE}"
    rf"|{_REGEX_VARIABLE}"
    rf"|{_REGEX_WILDCARD}"
    rf"|{_REGEX_DIMENSION_BREAKDOWN})"
)
_REGEX_DIMENSION_WITH_LABEL = rf"({_REGEX_DIMENSION}(\s+{_REGEX_LABEL})*)"
_REGEX_DIMENSIONS = (
    rf"{_REGEX_DIMENSION_WITH_LABEL}({_REGEX_SEPARATOR}{_REGEX_DIMENSION_WITH_LABEL})*"
)
_REGEX_DIMENSION_ELLIPSIS = (
    rf"({_REGEX_DIMENSION_WITH_LABEL}{_REGEX_SEPARATOR}\.\.\.\s*)"
)
_REGEX_SHAPE_EXPRESSION = rf"^({_REGEX_DIMENSIONS}|{_REGEX_DIMENSION_ELLIPSIS})$"
