from typing import Any
from unittest import TestCase

import numpy as np

from nptyping import (
    Bool,
    Float,
    Int,
    InvalidArgumentsError,
    NDArray,
    NPTypingError,
    Shape,
    UInt8,
)
from nptyping.error import InvalidDTypeError
from nptyping.typing_ import Literal


class NDArrayTest(TestCase):
    def test_isinstance_succeeds_if_shapes_match_exactly(self):

        # Trivial identity checks.
        self.assertIs(NDArray, NDArray)
        self.assertIs(NDArray[Shape["1, 1"], Any], NDArray[Shape["1, 1"], Any])

        # Tuples should not make any difference.
        self.assertIs(NDArray[Shape["1, 1"], Any], NDArray[(Shape["1, 1"], Any)])

        # Whitespaces should not make any difference.
        self.assertIs(NDArray[Shape["1,1"], Any], NDArray[(Shape[" 1 , 1 "], Any)])

        # Arguments may point to the default NDArray (any type, any shape).
        self.assertIs(NDArray, NDArray[Any, Any])
        self.assertIs(NDArray, NDArray[Shape["*, ..."], Any])

        self.assertIsNot(NDArray[Shape["1, 1"], Any], NDArray[Shape["1, 2"], Any])
        self.assertIsNot(
            NDArray[Shape["1, 1"], np.floating], NDArray[Shape["1, 1"], Any]
        )

    def test_invalid_arguments_raise_errors(self):
        with self.assertRaises(InvalidArgumentsError) as err:
            NDArray[Shape["1"], Any, "Not good"]
        self.assertIn("Not good", str(err.exception))

        with self.assertRaises(InvalidArgumentsError) as err:
            NDArray["Not a Shape Expression", Any]
        self.assertIn("Not a Shape Expression", str(err.exception))

        with self.assertRaises(InvalidArgumentsError) as err:
            NDArray["Not a valid argument"]
        self.assertIn("str", str(err.exception))

        with self.assertRaises(InvalidArgumentsError):
            NDArray[Any]

        with self.assertRaises(InvalidArgumentsError):
            NDArray[Shape["1"]]

        with self.assertRaises(InvalidArgumentsError):
            NDArray[UInt8]

        with self.assertRaises(InvalidDTypeError) as err:
            NDArray[Any, "Not a DType"]
        self.assertIn("Not a DType", str(err.exception))

    def test_valid_arguments_should_not_raise(self):
        NDArray
        NDArray[Any, Any]
        NDArray[Shape["1"], Any]
        NDArray[(Shape["1"], Any)]
        NDArray[(Literal["1"], Any)]

    def test_str(self):
        self.assertEqual("NDArray[Any, Any]", str(NDArray[Any, Any]))
        self.assertEqual("NDArray[Any, Any]", str(NDArray[Shape[" * , ... "], Any]))
        self.assertEqual(
            "NDArray[Shape['2, 2'], Any]", str(NDArray[Shape[" 2 , 2 "], Any])
        )
        self.assertEqual("NDArray[Any, UByte]", str(NDArray[Any, UInt8]))
        self.assertEqual("NDArray[Any, UByte]", str(NDArray[Any, np.uint8]))
        self.assertEqual(
            str(NDArray[Shape[" 2 , 2 "], Any]), repr(NDArray[Shape[" 2 , 2 "], Any])
        )

    def test_types_with_numpy_dtypes(self):
        self.assertIsInstance(np.array([42]), NDArray[Any, np.int_])
        self.assertIsInstance(np.array([42.0]), NDArray[Any, np.float_])
        self.assertIsInstance(np.array([np.uint8(42)]), NDArray[Any, np.uint8])
        self.assertIsInstance(np.array([True]), NDArray[Any, np.bool_])

    def test_types_with_nptyping_aliases(self):
        self.assertIsInstance(np.array([42]), NDArray[Any, Int])
        self.assertIsInstance(np.array([42.0]), NDArray[Any, Float])
        self.assertIsInstance(np.array([np.uint8(42)]), NDArray[Any, UInt8])
        self.assertIsInstance(np.array([True]), NDArray[Any, Bool])

    def test_recursive_structure_is_forbidden(self):
        with self.assertRaises(NPTypingError) as err:
            NDArray[Any, Int][Any, Int]
        self.assertEqual(
            "Type NDArray[Any, Int] is already parameterized", str(err.exception)
        )

    def test_ndarray_is_hashable(self):
        hash(NDArray)
        hash(NDArray[Any, Any])
        hash(NDArray[Shape["2, 2"], Any])

    def test_instantiation_is_forbidden(self):
        with self.assertRaises(NPTypingError):
            NDArray[Shape["2, 2"], Any]()

    def test_subclassing_is_forbidden(self):
        with self.assertRaises(NPTypingError):

            class C(NDArray):
                ...

    def test_changing_attributes_is_forbidden(self):
        with self.assertRaises(NPTypingError):
            NDArray[Any, Any].__args__ = (1, 2)

        with self.assertRaises(NPTypingError):
            NDArray[Any, Any].some_attr = 42
