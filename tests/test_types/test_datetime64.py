from datetime import datetime
from unittest import TestCase

import numpy

from nptyping import Datetime64


class TestDatetime64(TestCase):

    def test_isinstance(self):
        self.assertIsInstance(datetime.now(), Datetime64)
        self.assertIsInstance(numpy.datetime64(datetime.now()), Datetime64)

    def test_repr(self):
        self.assertEqual('Datetime64', repr(Datetime64))

    def test_type_of(self):
        self.assertEqual(Datetime64, Datetime64.type_of(datetime.now()))
