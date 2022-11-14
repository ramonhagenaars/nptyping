from typing import Any
from unittest import TestCase

import pandas as pd

from nptyping import DataFrame, InvalidArgumentsError
from nptyping import Structure as S
from nptyping.typing_ import Literal as L


class DataframeTest(TestCase):
    def test_isinstance_success(self):
        df = pd.DataFrame(
            {
                "x": [1, 2, 3],
                "y": [2.0, 3.0, 4.0],
                "z": ["a", "b", "c"],
            }
        )

        self.assertIsInstance(df, DataFrame[S["x: Int, y: Float, z: Obj"]])

    def test_isinstance_any(self):
        df = pd.DataFrame(
            {
                "x": [1, 2, 3],
                "y": [2.0, 3.0, 4.0],
                "z": ["a", "b", "c"],
            }
        )

        self.assertIsInstance(df, DataFrame[Any])

    def test_isinstance_fail(self):
        df = pd.DataFrame(
            {
                "x": [1, 2, 3],
                "y": [2.0, 3.0, 4.0],
                "z": ["a", "b", "c"],
            }
        )

        self.assertNotIsInstance(df, DataFrame[S["x: Float, y: Int, z: Obj"]])

    def test_string_is_aliased(self):
        df = pd.DataFrame(
            {
                "x": ["a", "b", "c"],
                "y": ["d", "e", "f"],
            }
        )

        self.assertIsInstance(df, DataFrame[S["x: Str, y: String"]])

    def test_isinstance_fail_with_random_type(self):
        self.assertNotIsInstance(42, DataFrame[S["x: Float, y: Int, z: Obj"]])

    def test_literal_is_allowed(self):
        DataFrame[L["x: Int, y: Int"]]

    def test_string_is_not_allowed(self):
        with self.assertRaises(InvalidArgumentsError):
            DataFrame["x: Int, y: Int"]

    def test_repr(self):
        self.assertEqual(
            "DataFrame[Structure['[x, y]: Int']]", repr(DataFrame[S["x: Int, y: Int"]])
        )
        self.assertEqual("DataFrame[Any]", repr(DataFrame))
        self.assertEqual("DataFrame[Any]", repr(DataFrame[Any]))

    def test_str(self):
        self.assertEqual("DataFrame[[x, y]: Int]", str(DataFrame[S["x: Int, y: Int"]]))
        self.assertEqual("DataFrame[Any]", str(DataFrame))
        self.assertEqual("DataFrame[Any]", str(DataFrame[Any]))
