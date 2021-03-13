from unittest import TestCase

import numpy as np

from nptyping import Object


class TestObject(TestCase):

    def test_repr(self):
        self.assertEqual('Object', repr(Object))

    def test_instance_check(self):
        self.assertIsInstance(np.array([1, 2, 3]), Object)
        self.assertIsInstance(np.int32(42), Object)
