from unittest import TestCase

import numpy as np
from nptyping import Int, SubArrayType
from nptyping.types._subarray_type import is_subarray_type


class TestSubArrayType(TestCase):
    def test_number_is_not_a_subarray_type(self):
        self.assertFalse(is_subarray_type(np.int32))

    def test_subarray_is_a_subarray_type(self):
        self.assertTrue(is_subarray_type(np.dtype((int, 4))))

    def test_structured_array_is_not_a_subarray_type(self):
        self.assertFalse(is_subarray_type(np.dtype([('x', int), ('y', int, (2, 3))])))

    def test_subarray_element_of_structured_array_is_a_structured_type(self):
        some_type = np.dtype([('x', int), ('y', int, (2, 3))])
        self.assertTrue(is_subarray_type(some_type.fields['y'][0]))

    def test_subarray_type_constructed_by_hand_is_equal_to_constructed_from_dtype(self):
        self.assertEqual(SubArrayType[Int[32], (4,)], SubArrayType[np.dtype((np.int32, 4))])

    def test_subarray_type_constructed_by_hand_is_not_equal_to_constructed_from_dtype_if_shape_doesnt_match(self):
        self.assertNotEqual(SubArrayType[np.int32, (4,)], SubArrayType[np.dtype((np.int32, (4, 1)))])

    def test_subarray_type_constructed_by_hand_is_not_equal_to_constructed_from_dtype_if_base_doesnt_match(self):
        self.assertNotEqual(SubArrayType[np.int16, (4,)], SubArrayType[np.dtype((np.int32, 4))])

    def test_subarray_dtype_is_an_instance_of_subarray_type(self):
        self.assertIsInstance(np.dtype((np.int32, 4)), SubArrayType[np.int32, (4,)])

    def test_subarray_dtype_is_not_an_instance_of_subarray_type_if_shape_doesnt_match(self):
        self.assertNotIsInstance(np.dtype((np.int32, 4)), SubArrayType[np.int32, (4, 1)])

    def test_subarray_dtype_is_not_an_instance_of_subarray_type_if_base_doesnt_match(self):
        self.assertNotIsInstance(np.dtype((np.int32, 4)), SubArrayType[np.int16, 4])

    def test_subarray_type_repr_with_no_parameters(self):
        self.assertEqual(str(SubArrayType), 'SubArrayType')

    def test_subarray_type_repr_with_parameters(self):
        self.assertEqual(str(SubArrayType[Int[16], (4,)]), 'SubArrayType[Int[16], (4,)]')

    def test_other_type_is_not_an_instance_of_subarray_type(self):
        self.assertNotIsInstance(Int[32], SubArrayType[Int[32], (1,)])

    def test_other_type_does_not_equal_subarray_type(self):
        self.assertNotEqual(SubArrayType[Int[32], (1,)], Int[32])

    def test_incompatible_parameters_to_subarray_type_raise_exception(self):
        with self.assertRaises(Exception):
            SubArrayType[Int[32]]
        with self.assertRaises(Exception):
            SubArrayType['bad arg']
