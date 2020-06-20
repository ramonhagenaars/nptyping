from datetime import timedelta
from unittest import TestCase

import numpy

from nptyping.types._timedelta64 import Timedelta64


class TestTimedelta64(TestCase):

    def test_isinstance(self):
        self.assertIsInstance(timedelta(days=1), Timedelta64)
        self.assertIsInstance(numpy.timedelta64(1), Timedelta64)

    def test_repr(self):
        self.assertEqual('Timedelta64', repr(Timedelta64))

    def test_type_of(self):
        self.assertEqual(Timedelta64, Timedelta64.type_of(timedelta(days=42)))
