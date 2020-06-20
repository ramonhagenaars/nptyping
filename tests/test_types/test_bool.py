from unittest import TestCase

import numpy

from nptyping import Bool


class TestBool(TestCase):

    def test_isinstance(self):
        self.assertIsInstance(True, Bool)
        self.assertIsInstance(False, Bool)

        self.assertIsInstance(numpy.bool_(True), Bool)
        self.assertIsInstance(numpy.bool_(False), Bool)

    def test_repr(self):
        self.assertEqual('Bool', repr(Bool))

    def test_bool_of(self):
        self.assertEqual(Bool, Bool.type_of(True))
        self.assertEqual(Bool, Bool.type_of(False))
        self.assertEqual(Bool, Bool.type_of(numpy.bool_))
        self.assertEqual(Bool, Bool.type_of(numpy.bool_(True)))
        self.assertEqual(Bool, Bool.type_of(numpy.bool_(False)))
        self.assertEqual(Bool, Bool.type_of(1))
