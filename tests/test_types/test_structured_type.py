from unittest import TestCase

import numpy as np
from nptyping import Int, StructuredType, Unicode, SubArrayType
from nptyping.types._structured_type import is_structured_type


class TestStructuredType(TestCase):

    def test_equality_of_basic_object_with_no_structure(self):
        self.assertEqual(StructuredType, StructuredType)

    def test_equality_of_two_structured_types(self):
        self.assertEqual(StructuredType[Int[32], Unicode[8]], StructuredType[Int[32], Unicode[8]])

    def test_inequality_of_two_structured_types(self):
        self.assertNotEqual(StructuredType[Int[32], Unicode[8], Int[16]], StructuredType[Int[32], Unicode[8]])

    def test_dtype_constructed_by_hand_is_an_instance_of_structured_type(self):
        self.assertIsInstance(np.dtype([('x', np.int32), ('y', np.int32)]), StructuredType[Int[32], Int[32]])

    def test_names_dont_matter_when_comparing_two_structured_types(self):
        self.assertEqual(StructuredType[np.dtype([('x', np.int32), ('y', np.int32)])], StructuredType[np.dtype([('a', np.int32), ('b', np.int32)])])

    def test_dtype_constructed_by_hand_is_not_an_instance_of_structured_type_if_fields_differ(self):
        self.assertNotIsInstance(np.dtype([('x', np.int32), ('y', np.int16)]), StructuredType[Int[32], Int[32]])

    def test_number_is_not_a_structured_type(self):
        self.assertFalse(is_structured_type(np.int32))

    def test_structured_array_is_a_structured_type(self):
        self.assertTrue(is_structured_type(np.dtype([('x', np.int32), ('y', np.int32, (2, 3))])))

    def test_structured_type_by_hand_instance_check(self):
        some_dtype = np.dtype([('x', np.int32), ('y', np.int32, 4)])
        self.assertIsInstance(some_dtype, StructuredType[Int[32], SubArrayType[Int[32], (4,)]])

    def test_structured_type_repr_with_no_parameters(self):
        self.assertEqual(str(StructuredType), 'StructuredType')

    def test_structured_type_repr_with_parameters(self):
        self.assertEqual(str(StructuredType[Int[16], SubArrayType[Int[32], (4,)]]),
                         'StructuredType[Int[16], SubArrayType[Int[32], (4,)]]')

    def test_structured_type_single_field(self):
        self.assertIsInstance(np.dtype([('x', np.int32)]), StructuredType[Int[32]])

    def test_other_type_is_not_an_instance_of_structured_type(self):
        self.assertNotIsInstance(Int[32], StructuredType[Int[32], Int[32]])

    def test_structured_type_derived_from_dtype_passes_instance_check(self):
        self.assertIsInstance(StructuredType[np.dtype([('x', np.int32), ('y', np.int32)])], StructuredType[Int[32], Int[32]])

    def test_structured_type_from_heterogenous_base_types(self):
        self.assertEqual(StructuredType[Int[32], np.int32], StructuredType[Int[32], Int[32]])

    def test_incompatible_parameters_to_structured_type_raise_exception(self):
        with self.assertRaises(Exception):
            StructuredType['bad arg']
