from unittest import TestCase

import numpy

from nptyping._hashed_subscriptable_type import HashedSubscriptableType


class TestHashedSubscriptableType(TestCase):

    def test_isinstance(self):
        class C(metaclass=HashedSubscriptableType):
            ...

        self.assertIs(C[42], C[42])
        self.assertIs(C[('Tuples', 'work', 'also')], C[('Tuples', 'work', 'also')])
        self.assertIs(C[['Even', 'lists', 'work']], C[['Even', 'lists', 'work']])
        self.assertIs(C[numpy.array([1, 2, 3])], C[numpy.array([1, 2, 3])])
        self.assertIsNot(C[42], C[42.])
