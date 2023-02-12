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
from abc import ABC
from typing import (
    Any,
    Dict,
    List,
)

from nptyping.base_meta_classes import ContainerMeta
from nptyping.nptyping_type import NPTypingType
from nptyping.structure_expression import (
    create_name_to_type_dict,
    normalize_structure_expression,
    validate_structure_expression,
)


class StructureMeta(ContainerMeta, implementation="Structure"):
    """
    Metaclass that is coupled to nptyping.Structure.
    """

    __args__ = tuple()

    def _validate_expression(cls, item: str) -> None:
        validate_structure_expression(item)

    def _normalize_expression(cls, item: str) -> str:
        return normalize_structure_expression(item)

    def _get_additional_values(cls, item: Any) -> Dict[str, Any]:
        return {
            "_type_per_name": create_name_to_type_dict(item),
            "_has_wildcard": item.replace(" ", "").endswith(",*"),
        }


class Structure(NPTypingType, ABC, metaclass=StructureMeta):
    """
    A container for structure expressions that describe the structured dtype of
    an array.

    Simple example:

    >>> Structure["x: Float, y: Float"]
    Structure['[x, y]: Float']

    """

    _type_per_name = {}
    _has_wildcard = False

    @classmethod
    def has_wildcard(cls) -> bool:
        """
        Returns whether this Structure has a wildcard for any other columns.
        :return: True if this Structure expresses "any other columns".
        """
        return cls._has_wildcard

    @classmethod
    def get_types(cls) -> List[str]:
        """
        Return a list of all types (strings) in this Structure.
        :return: a list of all types in this Structure.
        """
        return list(set(cls._type_per_name.values()))

    @classmethod
    def get_names(cls) -> List[str]:
        """
        Return a list of all names in this Structure.
        :return: a list of all names in this Structure.
        """
        return list(cls._type_per_name.keys())

    @classmethod
    def get_type(cls, name: str) -> str:
        """
        Get the type (str) that corresponds to the given name. For example for
        Structure["x: Float"], get_type("x") would give "Float".
        :param name: the name of which the type is to be returned.
        :return: the type as a string that corresponds to that name.
        """
        return cls._type_per_name[name]
