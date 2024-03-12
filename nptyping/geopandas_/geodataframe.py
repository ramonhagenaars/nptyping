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
from nptyping.geopandas_.typing_ import dtype_per_name
from nptyping.pandas_.dataframe import DataFrameMeta
from nptyping.structure import Structure
from nptyping.structure_expression import check_structure

try:
    import geopandas as gpd
except ImportError:  # pragma: no cover
    gpd = None  # type: ignore[misc, assignment]


class GeoDataFrameMeta(
    DataFrameMeta,
    SubscriptableMeta,
    InconstructableMeta,
    ImmutableMeta,
    FinalMeta,
    MaybeCheckableMeta,
    PrintableMeta,
    implementation="GeoDataFrame",
):
    """
    Metaclass that is coupled to nptyping.GeoDataFrame. It contains all actual logic
    such as instance checking.
    """

    def __instancecheck__(  # pylint: disable=bad-mcs-method-argument
        self, instance: Any
    ) -> bool:
        structure = self.__args__[0]

        if gpd is None:
            raise DependencyError(  # pragma: no cover
                "GeoPandas needs to be installed for instance checking."
            )

        if not isinstance(instance, gpd.GeoDataFrame):
            return False

        if structure is Any:
            return True

        structured_dtype = np.dtype(
            [(column, dtype.str) for column, dtype in instance.dtypes.items()]
        )
        return check_structure(structured_dtype, structure, dtype_per_name)

    @property
    def __module__(cls) -> str:
        return cls._get_module(inspect.stack(), "nptyping.geopandas_.geodataframe")


class GeoDataFrame(NPTypingType, ABC, metaclass=GeoDataFrameMeta):
    """
    An nptyping equivalent of geopandas GeoDataFrame.

    ## No arguments means a GeoDataFrame of any structure.
    >>> GeoDataFrame
    GeoDataFrame[Any]

    ## You can use Structure Expression.
    >>> from nptyping import GeoDataFrame, Structure
    >>> GeoDataFrame[Structure["x: Int, y: Int"]]
    GeoDataFrame[Structure['[x, y]: Int']]

    ## Instance checking can be done and the structure is also checked.
    >>> import geopandas as gpd
    >>> gdf = gpd.GeoDataFrame({'x': [1, 2, 3], 'y': [4., 5., 6.]})
    >>> isinstance(gdf, GeoDataFrame[Structure['x: Int, y: Float']])
    True
    >>> isinstance(gdf, GeoDataFrame[Structure['x: Float, y: Int']])
    False

    """

    __args__ = (Any,)
