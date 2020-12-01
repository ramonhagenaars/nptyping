from typing import Any, Optional
from unittest import TestCase

import numpy as np
from numpy.core.arrayprint import SubArrayFormat

from nptyping import NDArray, DEFAULT_INT_BITS, Int, Bool, Datetime64, StructuredType, SubArrayType
from nptyping.types._timedelta64 import Timedelta64


class TestNDArray(TestCase):

    def test_initialize_with_nothing(self):
        self.assertEqual((Any, ...), NDArray.shape)
        self.assertEqual(Any, NDArray._type)
        self.assertEqual((Any, ...), NDArray[(Any, ...)].shape)
        self.assertEqual(Any, NDArray[(Any, ...)]._type)
        self.assertEqual((Any, ...), NDArray[(Any, ...), Any].shape)
        self.assertEqual(Any, NDArray[(Any, ...), Any]._type)

    def test_initialize_with_size(self):
        self.assertEqual(1, len(NDArray[5].shape))
        self.assertEqual(5, NDArray[5].shape[0])
        self.assertEqual(Any, NDArray[5]._type)
        self.assertEqual(NDArray[5], NDArray[(5,)])
        self.assertEqual(NDArray[5], NDArray[(5,), Any])

    def test_initialize_with_any_size(self):
        self.assertEqual(1, len(NDArray[Any].shape))
        self.assertEqual(Any, NDArray[Any].shape[0])
        self.assertEqual(Any, NDArray[Any]._type)

    def test_initialize_with_type(self):
        self.assertEqual((Any, ...), NDArray[int].shape)
        self.assertEqual(Int[DEFAULT_INT_BITS], NDArray[int]._type)
        self.assertEqual(Int, NDArray[Int]._type)
        self.assertEqual(Bool, NDArray[Bool]._type)

    def test_initialize_with_size_and_type(self):
        self.assertEqual(1, len(NDArray[3, int].shape))
        self.assertEqual(3, NDArray[3, int].shape[0])
        self.assertEqual(Int[DEFAULT_INT_BITS], NDArray[3, int]._type)

    def test_initialize_with_only_sizes(self):
        self.assertEqual(3, len(NDArray[(2, 4, Any)].shape))
        self.assertEqual(2, NDArray[(2, 4, Any)].shape[0])
        self.assertEqual(4, NDArray[(2, 4, Any)].shape[1])
        self.assertEqual(Any, NDArray[(2, 4, Any)].shape[2])
        self.assertEqual(Any, NDArray[(2, 4, Any)]._type)
        self.assertEqual(NDArray[(2, 4, Any)], NDArray[2, 4, Any])

    def test_initialize_with_sizes_and_type(self):
        self.assertEqual(3, len(NDArray[(2, 4, Any), int].shape))
        self.assertEqual(2, NDArray[(2, 4, Any), int].shape[0])
        self.assertEqual(4, NDArray[(2, 4, Any), int].shape[1])
        self.assertEqual(Any, NDArray[(2, 4, Any), int].shape[2])
        self.assertEqual(Int[DEFAULT_INT_BITS], NDArray[(2, 4, Any), int]._type)

    def test_initialize_with_sizes_and_dtype(self):
        arr = NDArray[(2, 4, Any), np.dtype(int)]

        self.assertEqual(3, len(arr.shape))
        self.assertEqual(2, arr.shape[0])
        self.assertEqual(4, arr.shape[1])
        self.assertEqual(Any, arr.shape[2])
        self.assertEqual(Int[DEFAULT_INT_BITS], arr._type)

    def test_initialize_with_ndims(self):
        self.assertEqual((2, ...), NDArray[(2, ...), int].shape)

    def test_with_any_and_any(self):
        array_str = repr(NDArray[Any, Any])
        expected = 'NDArray[(typing.Any,), typing.Any]'
        self.assertEqual(expected, array_str)

    def test_invalid_initialization(self):
        with self.assertRaises(TypeError):
            NDArray['test']
        with self.assertRaises(TypeError):
            NDArray[(2, '2'), int]
        with self.assertRaises(TypeError):
            NDArray[(2, 2), 'int']
        with self.assertRaises(TypeError):
            NDArray[(2, 2, ...), int]

    def test_instance_check_dimension_sizes(self):
        arr2x2x2 = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        arr1x2x2 = np.array([[[1, 2], [3, 4]]])
        arr3x2x2 = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]], [[9, 10], [11, 12]]])
        arr2x2 = np.array([[1, 2], [3, 4]])

        self.assertTrue(isinstance(arr2x2x2, NDArray[(2, 2, 2), int]))
        self.assertTrue(not isinstance(arr1x2x2, NDArray[(2, 2, 2), int]))
        self.assertTrue(not isinstance(arr3x2x2, NDArray[(2, 2, 2), int]))
        self.assertTrue(not isinstance(arr2x2, NDArray[(2, 2, 2), int]))

    def test_instance_check_dimension_any(self):
        arr3x2x2 = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]], [[9, 10], [11, 12]]])
        arr2x2 = np.array([[1, 2], [3, 4]])

        self.assertTrue(isinstance(arr3x2x2, NDArray))
        self.assertTrue(isinstance(arr2x2, NDArray))
        self.assertTrue(isinstance(arr3x2x2, NDArray[int]))
        self.assertTrue(isinstance(arr2x2, NDArray[int]))

    def test_instance_check_types(self):
        arr2x2x2_float = np.array([[[1.0, 2.0], [3.0, 4.0]],
                                   [[5.0, 6.0], [7.0, 8.0]]])
        arr2x2x2 = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])

        self.assertTrue(isinstance(arr2x2x2_float, NDArray[(2, 2, 2), float]))
        self.assertTrue(not isinstance(arr2x2x2, NDArray[(2, 2, 2), str]))

    def test_instance_check_types_any(self):
        arr2x2x2_float = np.array([[[1.0, 2.0], [3.0, 4.0]],
                                   [[5.0, 6.0], [7.0, 8.0]]])
        arr2x2x2 = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        arr2x2 = np.array([[1, 2], [3, 4]])

        self.assertTrue(isinstance(arr2x2x2, NDArray[(2, 2, 2)]))
        self.assertTrue(isinstance(arr2x2x2_float, NDArray[(2, 2, 2)]))
        self.assertTrue(not isinstance(arr2x2, NDArray[(2, 2, 2)]))

    def test_instance_check_ndims(self):
        arr2x2x2 = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        arr2x2 = np.array([[1, 2], [3, 4]])
        arr3x2x2 = np.array([[[1, 2], [3, 4]],
                             [[5, 6], [7, 8]],
                             [[9, 10], [11, 12]]])

        self.assertTrue(isinstance(arr2x2, NDArray[(2, ...), int]))
        self.assertTrue(isinstance(arr2x2x2, NDArray[(2, ...), int]))
        self.assertTrue(not isinstance(arr3x2x2, NDArray[(2, ...), int]))

    def test_subclass_check(self):
        self.assertTrue(issubclass(NDArray[(2, 2, 2), int], NDArray[(2, 2, 2), int]))
        self.assertTrue(issubclass(NDArray[(2, 2, 2), int], NDArray))
        self.assertTrue(issubclass(NDArray[(2, 2, 2), int], NDArray[int]))
        self.assertTrue(not issubclass(NDArray[(2, 2, 2), int], NDArray[(2, 2, 3), int]))

    def test_repr_and_str(self):
        # These imports are needed for the evals to work.
        import typing
        from nptyping import Int

        arr_1a = NDArray[(2, 2), Int]
        arr_1b = eval(repr(arr_1a))

        arr_2a = NDArray[(typing.Any, ...), int]
        arr_2b = eval(repr(arr_2a))

        arr_3a = NDArray
        arr_3b = eval(repr(arr_3a))

        arr_4a = NDArray[5]
        arr_4b = eval(repr(arr_4a))

        self.assertEqual(arr_1a, arr_1b)
        self.assertEqual(arr_2a, arr_2b)
        self.assertEqual(arr_3a, arr_3b)
        self.assertEqual(arr_4a, arr_4b)

        self.assertEqual(str(arr_1a), repr(arr_1a))
        self.assertEqual(str(arr_2a), repr(arr_2a))
        self.assertEqual(str(arr_3a), repr(arr_3a))
        self.assertEqual(str(arr_4a), repr(arr_4a))

    def test_type_of(self):
        arr1 = np.array([1, 2, 3])
        arr2 = np.array([1, 2, '3'])
        arr3 = np.array([1, 2, 3.0])
        arr4 = np.array([1, 2, {}])
        arr5 = np.array([True, True, True])

        t1 = NDArray.type_of(arr1)
        t2 = NDArray.type_of(arr2)
        t3 = NDArray.type_of(arr3)
        t4 = NDArray.type_of(arr4)
        t5 = NDArray.type_of(arr5)

        self.assertIsInstance(arr1, t1)
        self.assertIsInstance(arr2, t2)
        self.assertIsInstance(arr3, t3)
        self.assertIsInstance(arr4, t4)
        self.assertIsInstance(arr5, t5)

    def test_hash_ndarray(self):
        # Hashing should not raise.
        hash(NDArray[(3,), int])

        # You should now be able to wrap an NDArray in an optional.
        Optional[NDArray[(3,), int]]
        Optional[NDArray]

    def test_instantiate(self):
        with self.assertRaises(TypeError) as err:
            NDArray([1, 2, 3])

        self.assertIn('NDArray', str(err.exception))

    def test_instance_check_with_np_types(self):
        self.assertIsInstance(np.array([[True, False], [True, False]]), NDArray[(Any, ...), Bool])
        self.assertNotIsInstance(np.array([[True, False], [True, 42]]), NDArray[(Any, ...), Bool])
        self.assertIsInstance(np.array([np.datetime64()]), NDArray[(Any, ...), Datetime64])
        self.assertIsInstance(np.array([np.timedelta64()]), NDArray[(Any, ...), Timedelta64])

    def test_instance_check_with_structured_types(self):
        some_dtype = np.dtype([('x', np.int32), ('y', np.int32, 4)])
        some_other_dtype = np.dtype([('x', np.int32), ('y', np.int32, 3)])
        self.assertIsInstance(np.zeros((1,), dtype=some_dtype), NDArray[(Any, ...), some_dtype])
        self.assertNotIsInstance(np.zeros((1,), dtype=some_dtype), NDArray[(Any, ...), some_other_dtype])
        self.assertIsInstance(np.zeros((1,), dtype=some_dtype), NDArray[(Any, ...), StructuredType[Int[32], SubArrayType[Int[32], (4,)]]])
