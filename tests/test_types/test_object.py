from unittest import TestCase

from nptyping import Object


class TestObject(TestCase):

    def test_repr(self):
        self.assertEqual('Object', repr(Object))
