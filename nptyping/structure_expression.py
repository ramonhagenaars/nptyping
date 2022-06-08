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
from collections import Counter, defaultdict
from difflib import get_close_matches
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Mapping,
    Union,
)

import numpy as np

from nptyping.error import InvalidStructureError
from nptyping.typing_ import StructureExpression

if TYPE_CHECKING:
    from nptyping.structure import Structure  # pragma: no cover


def validate_structure_expression(
    structure_expression: Union[StructureExpression, Any]
) -> None:
    """
    Validate the given structure_expression and raise an InvalidStructureError
    if it is deemed invalid.
    :param structure_expression: the structure expression in question.
    :return: None.
    """
    if structure_expression is not Any:
        if not re.match(_REGEX_STRUCTURE_EXPRESSION, structure_expression):
            raise InvalidStructureError(
                f"'{structure_expression}' is not a valid structure expression."
            )
        _validate_structure_expression_contains_no_multiple_field_names(
            structure_expression
        )


def check_structure(
    structured_dtype: np.dtype,  # type: ignore[type-arg]
    target: "Structure",
    type_per_name: Dict[str, type],
) -> bool:
    """
    Check the given structured_dtype against the given target Structure and
    return whether it corresponds (True) or not (False). The given dictionary
    contains the vocabulary context for the check.
    :param structured_dtype: the dtype in question.
    :param target: the target Structure that is checked against.
    :param type_per_name: a dict that holds the types by their names as they
    occur in a structure expression.
    :return: True if the given dtype is valid with the given target.
    """
    fields: Mapping[str, Any] = structured_dtype.fields or {}  # type: ignore[assignment]
    for name, dtype_tuple in fields.items():
        dtype = dtype_tuple[0]
        target_type_name = target.get_type(name)
        check_type_name(target_type_name, type_per_name)
        target_type = type_per_name[target_type_name]
        if not issubclass(dtype.type, target_type):
            return False
    return True


def check_type_names(structure: "Structure", type_per_name: Dict[str, type]) -> None:
    """
    Check the given structure for any invalid type names in the given context
    of type_per_name. Raises an InvalidStructureError if a type name is
    invalid.
    :param structure: the Structure that is checked.
    :param type_per_name: the context that determines which type names are valid.
    :return: None.
    """
    for type_ in structure.get_types():
        check_type_name(type_, type_per_name)


def check_type_name(type_name: str, type_per_name: Dict[str, type]) -> None:
    """
    Check if the given type_name is in type_per_name and raise a meaningful
    error if not.
    :param type_name: the key that is checked to be in type_per_name.
    :param type_per_name: a dict that is looked in for type_name.
    :return: None.
    """
    if type_name not in type_per_name:
        close_matches = get_close_matches(
            type_name, type_per_name.keys(), 3, cutoff=0.4
        )
        close_matches_str = ", ".join(f"'{match}'" for match in close_matches)
        extra_help = ""
        if len(close_matches) > 1:
            extra_help = f" Did you mean one of {close_matches_str}?"
        elif close_matches:
            extra_help = f" Did you mean {close_matches_str}?"
        raise InvalidStructureError(  # pylint: disable=raise-missing-from
            f"Type '{type_name}' is not valid in this context.{extra_help}"
        )


def normalize_structure_expression(
    structure_expression: StructureExpression,
) -> StructureExpression:
    """
    Normalize the given structure expression, e.g. by removing whitespaces,
    making similar expressions look the same.
    :param structure_expression: the structure expression that is to be normalized.
    :return: a normalized structure expression.
    """
    structure_expression = re.sub(r"\s*", "", structure_expression)
    type_to_names_dict = _create_type_to_names_dict(structure_expression)
    normalized_structure_expression = _type_to_names_dict_to_str(type_to_names_dict)
    return normalized_structure_expression.replace(",", ", ")


def create_name_to_type_dict(
    structure_expression: StructureExpression,
) -> Dict[str, str]:
    """
    Create a dict with a name as key and a type (str) as value from the given
    structure expression. Structure["x: Int, y: Float"] would yield
    {"x: "Int", "y": "Float"}.
    :param structure_expression: the structure expression from which the dict
    is extracted.
    :return: a dict with names and their types, both as strings.
    """
    type_to_names_dict = _create_type_to_names_dict(structure_expression)
    return {
        name.strip(): type_.strip()
        for type_, names in type_to_names_dict.items()
        for name in names
    }


def _validate_structure_expression_contains_no_multiple_field_names(
    structure_expression: StructureExpression,
) -> None:
    # Validate that there are not multiple occurrences of the same field names.
    matches = re.findall(_REGEX_FIELD, re.sub(r"\s*", "", structure_expression))
    field_name_combinations = [match[0].split(":")[0] for match in matches]
    field_names: List[str] = []
    for field_name_combination in field_name_combinations:
        field_name_combination_match = re.match(
            _REGEX_FIELD_NAMES_COMBINATION, field_name_combination
        )
        if field_name_combination_match:
            field_names += field_name_combination_match.group(2).split(_SEPARATOR)
        else:
            field_names.append(field_name_combination)
    field_name_counter = Counter(field_names)
    field_names_occurring_multiple_times = [
        field_name for field_name, amount in field_name_counter.items() if amount > 1
    ]
    if field_names_occurring_multiple_times:
        # If there are multiple, just raise about the first. Otherwise the
        # error message gets bloated.
        field_name_under_fire = field_names_occurring_multiple_times[0]
        raise InvalidStructureError(
            f"Field names may occur only once in a structure expression."
            f" Field name '{field_name_under_fire}' occurs"
            f" {field_name_counter[field_name_under_fire]} times in"
            f" '{structure_expression}'."
        )


def _create_type_to_names_dict(
    structure_expression: StructureExpression,
) -> Dict[str, List[str]]:
    # Create a dictionary with field names per type, sorted by type and then by
    # name.
    names_per_type: Dict[str, List[str]] = defaultdict(list)
    for field_match in re.findall(_REGEX_FIELD, structure_expression):
        field_name_combination, field_type = field_match[0].split(_FIELD_TYPE_POINTER)
        field_name_combination_match = re.match(
            _REGEX_FIELD_NAMES_COMBINATION, field_name_combination
        )
        if field_name_combination_match:
            field_names = field_name_combination_match.group(2).split(_SEPARATOR)
        else:
            field_names = [field_name_combination]
        names_per_type[field_type] += field_names
    return {
        field_type: sorted(names_per_type[field_type])
        for field_type in sorted(names_per_type.keys())
    }


def _type_to_names_dict_to_str(type_to_names_dict: Dict[str, List[str]]) -> str:
    # Turn the given dict into a structure expression.
    field_strings = []
    for field_type, field_names in type_to_names_dict.items():
        field_names_joined = f"{_SEPARATOR}".join(field_names)
        if len(field_names) > 1:
            field_names_joined = f"[{field_names_joined}]"
        field_strings.append(f"{field_names_joined}{_FIELD_TYPE_POINTER} {field_type}")
    return f"{_SEPARATOR}".join(field_strings)


_SEPARATOR = ","
_FIELD_TYPE_POINTER = ":"
_REGEX_SEPARATOR = rf"(\s*{_SEPARATOR}\s*)"
_REGEX_FIELD_NAME = r"(\s*[a-zA-Z]\w*\s*)"
_REGEX_FIELD_NAMES = rf"({_REGEX_FIELD_NAME}({_REGEX_SEPARATOR}{_REGEX_FIELD_NAME})+)"
_REGEX_FIELD_NAMES_COMBINATION = rf"(\s*\[{_REGEX_FIELD_NAMES}\]\s*)"
_REGEX_FIELD_LEFT = rf"({_REGEX_FIELD_NAME}|{_REGEX_FIELD_NAMES_COMBINATION})"
_REGEX_FIELD_TYPE = r"(\s*[a-zA-Z]\w*\s*)"
_REGEX_FIELD_TYPE_WILDCARD = r"(\s*\*\s*)"
_REGEX_FIELD_RIGHT = rf"({_REGEX_FIELD_TYPE}|{_REGEX_FIELD_TYPE_WILDCARD})"
_REGEX_FIELD_TYPE_POINTER = rf"(\s*{_FIELD_TYPE_POINTER}\s*)"
_REGEX_FIELD = (
    rf"(\s*{_REGEX_FIELD_LEFT}{_REGEX_FIELD_TYPE_POINTER}{_REGEX_FIELD_RIGHT}\s*)"
)
_REGEX_STRUCTURE_EXPRESSION = rf"^({_REGEX_FIELD}({_REGEX_SEPARATOR}{_REGEX_FIELD})*)$"
