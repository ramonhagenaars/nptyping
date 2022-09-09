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
from typing import Any, Tuple

import numpy as np

from nptyping import InvalidArgumentsError
from nptyping.base_meta_classes import (
    FinalMeta,
    ImmutableMeta,
    InconstructableMeta,
    MaybeCheckableMeta,
    PrintableMeta,
    SubscriptableMeta,
)
from nptyping.error import DependencyError
from nptyping.nptyping_type import NPTypingType
from nptyping.structure import Structure
from nptyping.structure_expression import check_structure
from nptyping.typing_ import dtype_per_name

try:
    import pandas as pd
except ImportError:  # pragma: no cover
    pd = None  # type: ignore[misc, assignment]


class DataFrameMeta(
    SubscriptableMeta,
    InconstructableMeta,
    ImmutableMeta,
    FinalMeta,
    MaybeCheckableMeta,
    PrintableMeta,
    implementation="DataFrame",
):
    """
    Metaclass that is coupled to nptyping.DataFrame. It contains all actual logic
    such as instance checking.
    """

    __args__: Tuple[Structure]
    _parameterized: bool

    def __instancecheck__(  # pylint: disable=bad-mcs-method-argument
        self, instance: Any
    ) -> bool:
        structure = self.__args__[0]

        if pd is None:
            raise DependencyError(  # pragma: no cover
                "Pandas needs to be installed for instance checking. Use `pip "
                "install nptyping[pandas]` or `pip install nptyping[complete]`"
            )

        if not isinstance(instance, pd.DataFrame):
            return False

        structured_dtype = np.dtype(
            [(column, dtype.str) for column, dtype in instance.dtypes.items()]
        )
        return check_structure(structured_dtype, structure, dtype_per_name)

    def _get_item(cls, item: Any) -> Tuple[Structure]:
        cls._check_item(item)
        return (Structure[getattr(item, "__args__")[0]],)

    def __str__(cls) -> str:
        shape = cls.__args__[0]
        shape_expression = shape.__args__[0]
        return f"{cls.__name__}[{shape_expression}]"

    def __repr__(cls) -> str:
        shape = cls.__args__[0]
        return f"{cls.__name__}[{shape}]"

    def _check_item(cls, item: Any) -> None:
        # Check if the item is what we expect and raise if it is not.
        if not hasattr(item, "__args__"):
            raise InvalidArgumentsError(f"Unexpected argument of type {type(item)}.")


class DataFrame(NPTypingType, ABC, metaclass=DataFrameMeta):
    __args__ = (Any,)
