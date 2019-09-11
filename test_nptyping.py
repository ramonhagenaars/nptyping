from unittest import TestCase
import numpy as np
from nptyping import Array


class NPTypingTestSuite(TestCase):
    def test_isinstance(self):
        arr = np.array([[1, 2, 3],
                        [4, 5, 6],
                        [7, 8, 9],
                        [8, 7, 6]])

        self.assertTrue(isinstance(arr, Array))
        self.assertTrue(isinstance(arr, Array[int, 4, ...]))
        self.assertTrue(isinstance(arr, Array[int, 4]))
        self.assertTrue(isinstance(arr, Array[int, 4, None]))
        self.assertTrue(isinstance(arr, Array[int]))
        self.assertTrue(isinstance(arr, Array[int, ...]))
        self.assertTrue(isinstance(arr, Array[int, ..., 3]))
        self.assertTrue(isinstance(arr, Array[int, ..., ...]))
        self.assertTrue(not isinstance(arr, Array[int, 5, ...]))
        self.assertTrue(not isinstance(arr, Array[int, ..., 5]))
        self.assertTrue(not isinstance(arr, Array[int, 5, 5]))

        self.assertTrue(isinstance(np.array([1.0, 2.0, 3.0]), Array[float]))
        self.assertTrue(not isinstance(np.array([1.0, 2.0, 3.0]), Array[int]))
        self.assertTrue(isinstance(np.array([1.0, 2.0, 3.0]), Array))
        self.assertTrue(isinstance(np.array([]), Array[int]))

        self.assertTrue(isinstance(np.array(['1', '22', '333']), Array[str]))

    def test_heterogeneous_array(self):
        dtype = [('a', float), ('b', float), ('c', int), ('d', str)]
        a = np.array(
            [
                (1.0, 2.0, 3, '4'),
                (5.0, 6.0, 7, '8')
            ],
            dtype=dtype)

        self.assertTrue(isinstance(a, Array[float, float, int, str, 2]))
        self.assertTrue(isinstance(a, Array[float, float, int, str, ...]))
        self.assertTrue(isinstance(a, Array[float, float, int, str]))
        self.assertTrue(not isinstance(a, Array[float, int, int, str, 2]))
        self.assertTrue(not isinstance(a, Array[float, float, str, 2]))
        self.assertTrue(not isinstance(a, Array[float, float, str, 3]))
        with self.assertRaises(TypeError):
            Array[float, float, int, 'should be an int']

        dtype = [('a', int), ('b', int), ('c', int), ('d', int)]
        a = np.array(
            [
                (1, 2, 3, 4),
                (11, 22, 33, 44)
            ],
            dtype=dtype)

    def test_identity(self):
        self.assertTrue(Array is Array)
        self.assertTrue(Array[int] is Array[int])
        self.assertTrue(Array[int, 1, 1] is Array[int, 1, 1])

    def test_empty_arg(self):
        with self.assertRaises(TypeError):
            Array[tuple()]

    def test_instantiation(self):
        with self.assertRaises(TypeError):
            Array()
