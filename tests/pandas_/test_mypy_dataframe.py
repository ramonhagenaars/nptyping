import sys
from unittest import TestCase, skipIf

from tests.test_helpers.check_mypy_on_code import check_mypy_on_code


class MyPyDataFrameTest(TestCase):
    @skipIf(sys.version_info.minor <= 7, "MyPy does not work with DataFrame on 3.7")
    def test_mypy_accepts_dataframe(self):
        exit_code, stdout, stderr = check_mypy_on_code(
            """
            from nptyping import DataFrame, Structure as S
            import pandas as pd


            df: DataFrame[S["x: Int, y: Int"]] = pd.DataFrame({"x": [1], "y": [1]})
        """
        )
        self.assertEqual(0, exit_code, stdout)

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

    # FIXME: add more tests here...
