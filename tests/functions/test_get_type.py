from unittest import TestCase

import numpy as np

from nptyping import get_type, Int32, Float64, Int8, Int16, Int64


class TestGetType(TestCase):

    def test_get_type_int(self):
        self.assertEqual(Int32, get_type(42))

    def test_get_type_float(self):
        self.assertEqual(Float64, get_type(42.0))

    def test_get_type_numpy_type(self):
        self.assertEqual(Int8, get_type(np.int8))
        self.assertEqual(Int16, get_type(np.int16))
        self.assertEqual(Int32, get_type(np.int32))
        self.assertEqual(Int64, get_type(np.int64))
