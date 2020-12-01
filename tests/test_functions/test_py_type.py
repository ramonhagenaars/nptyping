from datetime import datetime, timedelta
from unittest import TestCase

import numpy as np

from nptyping import py_type


class TestPyType(TestCase):

    def test_py_type(self):
        self.assertIs(int, py_type(np.dtype(int)))
        self.assertIs(str, py_type(np.dtype(str)))
        self.assertIs(object, py_type(np.dtype(object)))
        self.assertIs(float, py_type(np.dtype(float)))

        self.assertIs(int, py_type(np.int))
        self.assertIs(int, py_type(np.int16))
        self.assertIs(int, py_type(np.int32))
        self.assertIs(int, py_type(np.int64))

        self.assertIs(int, py_type(np.uint))
        self.assertIs(int, py_type(np.uint16))
        self.assertIs(int, py_type(np.uint32))
        self.assertIs(int, py_type(np.uint64))

        self.assertIs(float, py_type(np.float))
        self.assertIs(float, py_type(np.float16))
        self.assertIs(float, py_type(np.float32))
        self.assertIs(float, py_type(np.float64))

        self.assertIs(datetime, py_type(np.datetime64))
        self.assertIs(timedelta, py_type(np.timedelta64))
