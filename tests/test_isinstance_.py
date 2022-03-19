from typing import Any
from unittest import TestCase

import numpy as np

from nptyping import NDArray, Shape


class IsInstanceTest(TestCase):
    def test_isinstance_succeeds_if_shapes_match_exactly(self):
        self.assertIsInstance(
            np.random.randn(2),
            NDArray[Any, Shape["2"]],
        )
        self.assertIsInstance(
            np.random.randn(2, 2),
            NDArray[Any, Shape["2, 2"]],
        )

    def test_isinstance_fails_if_shape_size_dont_match(self):
        self.assertNotIsInstance(
            np.random.randn(2, 2),
            NDArray[Any, Shape["2, 3"]],
        )

    def test_isinstance_fails_if_nr_of_shapes_dont_match(self):
        self.assertNotIsInstance(
            np.random.randn(2, 2),
            NDArray[Any, Shape["2, 2, 2"]],
        )
        self.assertNotIsInstance(
            np.random.randn(2, 2),
            NDArray[Any, Shape["2"]],
        )

    def test_isinstance_succeeds_if_variables_can_be_assigned(self):
        self.assertIsInstance(
            np.random.randn(3, 2),
            NDArray[Any, Shape["Axis1, Axis2"]],
        )
        self.assertIsInstance(
            np.random.randn(3, 2),
            NDArray[Any, Shape["Axis, 2"]],
            "Combinations of variables and values should work.",
        )
        self.assertIsInstance(
            np.random.randn(2),
            NDArray[Any, Shape["VaR14bLe_"]],
            "Anything that starts with an uppercase letter is a variable.",
        )

    def test_isinstance_fails_if_variables_cannot_be_assigned(self):
        self.assertNotIsInstance(
            np.random.randn(3, 2),
            NDArray[Any, Shape["Axis1, Axis1"]],
        )

    def test_isinstance_succeeds_with_wildcards(self):
        self.assertIsInstance(
            np.random.randn(4),
            NDArray[Any, Shape["*"]],
        )
        self.assertIsInstance(
            np.random.randn(4, 4),
            NDArray[Any, Shape["*, *"]],
        )

    def test_isinstance_succeeds_with_0d_arrays(self):
        self.assertIsInstance(
            np.array([]),
            NDArray[Any, Shape["0"]],
        )

    def test_isinstance_succeeds_with_ellipsis(self):
        self.assertIsInstance(
            np.array([[[[[[0]]]]]]),
            NDArray[Any, Shape["1, ..."]],
            "This should match with an array of any dimensions of size 1.",
        )
        self.assertIsInstance(
            np.array([[[[[[0, 0, 0]]]]]]),
            NDArray[Any, Shape["*, ..."]],
            "This should match with an array of any dimensions of any size.",
        )

    def test_isinstance_fails_with_ellipsis(self):
        self.assertNotIsInstance(
            np.array([[[[[[0, 0]]]]]]),
            NDArray[Any, Shape["1, ..."]],
            "This should match with an array of any dimensions of size 1.",
        )

    def test_isinstance_succeeds_with_dim_breakdown(self):
        self.assertIsInstance(
            np.random.randn(3, 2),
            NDArray[Any, Shape["3, [x, y]"]],
        )
        self.assertIsInstance(
            np.random.randn(3, 2),
            NDArray[Any, Shape["[obj1, obj2, obj3], [x, y]"]],
        )

    def test_isinstance_fails_with_dim_breakdown(self):
        self.assertNotIsInstance(
            np.random.randn(3, 2),
            NDArray[Any, Shape["3, [x, y, z]"]],
        )

    def test_isinstance_succeeds_with_labels(self):
        self.assertIsInstance(
            np.random.randn(100, 5),
            NDArray[Any, Shape["100 assets, [id, age, type, x, y]"]],
        )
        self.assertIsInstance(
            np.random.randn(100, 5),
            NDArray[Any, Shape["* assets, [id, age, type, x, y]"]],
        )
        self.assertIsInstance(
            np.random.randn(100, 5),
            NDArray[Any, Shape["N assets, [id, age, type, x, y]"]],
        )
