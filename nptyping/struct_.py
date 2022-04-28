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
from abc import ABC

from nptyping.nptyping_type import NPTypingType

from nptyping.base_meta_classes import ContainerMeta


class StructMeta(ContainerMeta, name="Struct"):
    """
    Metaclass that is coupled to nptyping.Struct.
    """

    def _validate_expression(cls, item: str) -> None:
        ...

    def _normalize_expression(cls, item: str) -> str:
        return item

    # def _get_additional_values(cls, item: Any) -> Dict[str, Any]:
    #     dim_strings = get_dimensions(item)
    #     dim_string_without_labels = remove_labels(dim_strings)
    #     return {"prepared_args": dim_string_without_labels}


class Struct(NPTypingType, ABC, metaclass=StructMeta):
    # Struct["x: float, y: int, z: float"]
    # Struct["[x, z]: float, y: int"]
    __args__ = ("*, ...",)
    prepared_args = "*, ..."
