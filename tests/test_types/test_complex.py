from unittest import TestCase

from nptyping import Complex128


class TestComplex(TestCase):

    def test_repr(self):
        self.assertEqual('Complex128', repr(Complex128))
