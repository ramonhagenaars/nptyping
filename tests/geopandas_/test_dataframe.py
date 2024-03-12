from typing import Any
from unittest import TestCase

import geopandas as gpd
from nptyping import InvalidArgumentsError, GeoDataFrame
from nptyping import Structure as S
from nptyping.typing_ import Literal as L
from shapely.geometry import Point


class DataframeTest(TestCase):
    def test_isinstance_success(self):
        gdf = gpd.GeoDataFrame(
            {
                "x": [1, 2, 3],
                "y": [2.0, 3.0, 4.0],
                "z": [Point(0, 0), Point(1, 1), Point(2, 2)],
            }
        )

        self.assertIsInstance(gdf, GeoDataFrame[S["x: Int, y: Float, z: Obj"]])

    def test_isinstance_any(self):
        gdf = gpd.GeoDataFrame(
            {
                "x": [1, 2, 3],
                "y": [2.0, 3.0, 4.0],
                "z": ["a", "b", "c"],
            }
        )

        self.assertIsInstance(gdf, GeoDataFrame[Any])

    def test_isinstance_fail(self):
        gdf = gpd.GeoDataFrame(
            {
                "x": [1, 2, 3],
                "y": [2.0, 3.0, 4.0],
                "z": ["a", "b", "c"],
            }
        )

        self.assertNotIsInstance(gdf, GeoDataFrame[S["x: Float, y: Int, z: Obj"]])

    def test_string_is_aliased(self):
        gdf = gpd.GeoDataFrame(
            {
                "x": ["a", "b", "c"],
                "y": ["d", "e", "f"],
            }
        )

        self.assertIsInstance(gdf, GeoDataFrame[S["x: Str, y: String"]])

    def test_isinstance_fail_with_random_type(self):
        self.assertNotIsInstance(42, GeoDataFrame[S["x: Float, y: Int, z: Obj"]])

    def test_literal_is_allowed(self):
        GeoDataFrame[L["x: Int, y: Int"]]

    def test_string_is_not_allowed(self):
        with self.assertRaises(InvalidArgumentsError):
            GeoDataFrame["x: Int, y: Int"]

    def test_repr(self):
        self.assertEqual(
            "GeoDataFrame[Structure['[x, y]: Int']]", repr(GeoDataFrame[S["x: Int, y: Int"]])
        )
        self.assertEqual("GeoDataFrame[Any]", repr(GeoDataFrame))
        self.assertEqual("GeoDataFrame[Any]", repr(GeoDataFrame[Any]))

    def test_str(self):
        self.assertEqual("GeoDataFrame[[x, y]: Int]", str(GeoDataFrame[S["x: Int, y: Int"]]))
        self.assertEqual("GeoDataFrame[Any]", str(GeoDataFrame))
        self.assertEqual("GeoDataFrame[Any]", str(GeoDataFrame[Any]))
