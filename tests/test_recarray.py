from typing import Any
from unittest import TestCase

import numpy as np

from nptyping import (
    Int32,
    NDArray,
    RecArray,
    Shape,
    Structure,
)
from nptyping.error import InvalidArgumentsError


class RecArrayTest(TestCase):
    def test_isinstance_succeeds_if_shape_and_structure_match(self):
        arr = np.array([("William", 23)], dtype=[("name", "U8"), ("age", "i4")])

        self.assertNotIsInstance(arr, RecArray)

        rec_arr = arr.view(np.recarray)

        self.assertIsInstance(rec_arr, RecArray)
        self.assertIsInstance(
            rec_arr, RecArray[Shape["1"], Structure["name: Str, age: Int32"]]
        )
        self.assertIsInstance(
            rec_arr, NDArray[Shape["1"], Structure["name: Str, age: Int32"]]
        )

    def test_rec_array_enforces_structure(self):
        with self.assertRaises(InvalidArgumentsError) as err:
            RecArray[Any, Int32]

        self.assertEqual(
            "Unexpected argument <class 'numpy.int32'>. Expecting a Structure.",
            str(err.exception),
        )

    def test_rec_array_allows_any(self):
        arr = np.array([("Billy", 23)], dtype=[("name", "U8"), ("age", "i4")])
        rec_arr = arr.view(np.recarray)

        self.assertIsInstance(rec_arr, RecArray[Any, Any])
