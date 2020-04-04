from unittest import TestCase

import numpy as np

from nptyping.py_type import py_type


class TestPyType(TestCase):

    def test_py_type(self):
        self.assertEqual(int, py_type(np.dtype(int)))
        self.assertEqual(str, py_type(np.dtype(str)))
        self.assertEqual(object, py_type(np.dtype(object)))
        self.assertEqual(float, py_type(np.dtype(float)))

        self.assertEqual(int, py_type(np.int))
        self.assertEqual(int, py_type(np.int16))
        self.assertEqual(int, py_type(np.int32))
        self.assertEqual(int, py_type(np.int64))

        self.assertEqual(float, py_type(np.float))
        self.assertEqual(float, py_type(np.float16))
        self.assertEqual(float, py_type(np.float32))
        self.assertEqual(float, py_type(np.float64))
