import pydoc
from unittest import TestCase

from nptyping import (
    DataFrame,
    Int,
    NDArray,
    RecArray,
    Shape,
    Structure,
)


class HelpTextsTest(TestCase):
    def test_help_ndarray(self):
        def func(arr: NDArray[Shape["2, 2"], Int]):
            ...

        help_text = pydoc.render_doc(func)

        self.assertIn("arr: NDArray[Shape['2, 2'], Int]", help_text)
        self.assertEqual("nptyping.ndarray", NDArray.__module__)

    def test_help_recdarray(self):
        def func(arr: RecArray[Shape["2, 2"], Structure["[x, y]: Float"]]):
            ...

        help_text = pydoc.render_doc(func)

        self.assertIn(
            "arr: RecArray[Shape['2, 2'], Structure['[x, y]: Float']]", help_text
        )
        self.assertEqual("nptyping.recarray", RecArray.__module__)

    def test_help_dataframe(self):
        def func(df: DataFrame[Structure["[x, y]: Float"]]):
            ...

        help_text = pydoc.render_doc(func)

        self.assertIn("df: DataFrame[Structure['[x, y]: Float']]", help_text)
        self.assertEqual("nptyping.pandas_.dataframe", DataFrame.__module__)
