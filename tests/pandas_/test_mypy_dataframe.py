from unittest import TestCase

from tests.test_helpers.check_mypy_on_code import check_mypy_on_code


class MyPyDataFrameTest(TestCase):
    def test_mypy_accepts_dataframe(self):
        exit_code, stdout, stderr = check_mypy_on_code(
            """
            from nptyping import DataFrame, Structure as _
            import pandas as pd


            df: DataFrame[_["x: Int, y: Int"]] = pd.DataFrame({"x": [1], "y": [1]})
        """
        )
        self.assertEqual(0, exit_code, stdout)

    # FIXME: add more tests here...
