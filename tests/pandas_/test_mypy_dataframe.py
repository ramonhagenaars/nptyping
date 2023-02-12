import sys
from unittest import TestCase, skipUnless

from tests.test_helpers.check_mypy_on_code import check_mypy_on_code


class MyPyDataFrameTest(TestCase):
    @skipUnless(7 < sys.version_info.minor, "MyPy does not work with DataFrame on 3.7")
    def test_mypy_accepts_dataframe(self):
        exit_code, stdout, stderr = check_mypy_on_code(
            """
            from nptyping import DataFrame, Structure as S
            import pandas as pd


            df: DataFrame[S["x: Int, y: Int"]] = pd.DataFrame({"x": [1], "y": [1]})
        """
        )
        self.assertEqual(0, exit_code, stdout)

    @skipUnless(7 < sys.version_info.minor, "MyPy does not work with DataFrame on 3.7")
    def test_mypy_disapproves_dataframe_with_wrong_function_arguments(self):
        exit_code, stdout, stderr = check_mypy_on_code(
            """
            from typing import Any
            import numpy as np
            from nptyping import DataFrame, Structure as S


            def func(_: DataFrame[S["x: Float, y: Float"]]) -> None:
                ...


            func("Not an array...")
        """
        )

        self.assertIn('Argument 1 to "func" has incompatible type "str"', stdout)
        self.assertIn('expected "DataFrame[Any]"', stdout)
        self.assertIn("Found 1 error in 1 file", stdout)

    @skipUnless(7 < sys.version_info.minor, "MyPy does not work with DataFrame on 3.7")
    def test_mypy_knows_of_dataframe_methods(self):
        # If MyPy knows of some arbitrary DataFrame methods, we can assume that
        # code completion works.
        exit_code, stdout, stderr = check_mypy_on_code(
            """
            from typing import Any
            from nptyping import DataFrame


            df: DataFrame[Any]
            df.shape
            df.dtypes
            df.values
            df.boxplot
            df.filter
        """
        )

        self.assertEqual(0, exit_code, stdout)
