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
        self.assertIs(NDArray[Any, Shape["1, 1"]], NDArray[Any, Shape["1, 1"]])

        # Tuples should not make any difference.
        self.assertIs(NDArray[Any, Shape["1, 1"]], NDArray[(Any, Shape["1, 1"])])

        # Whitespaces should not make any difference.
        self.assertIs(NDArray[Any, Shape["1,1"]], NDArray[(Any, Shape[" 1 , 1 "])])

        # Arguments may point to the default NDArray (any type, any shape).
        self.assertIs(NDArray, NDArray[Any, Any])
        self.assertIs(NDArray, NDArray[Any, Shape["*, ..."]])

        self.assertIsNot(NDArray[Any, Shape["1, 1"]], NDArray[Any, Shape["1, 2"]])
        self.assertIsNot(
            NDArray[np.floating, Shape["1, 1"]], NDArray[Any, Shape["1, 1"]]
        )

    def test_invalid_arguments_raise_errors(self):
        with self.assertRaises(InvalidArgumentsError) as err:
            NDArray[Any, Shape["1"], "Not good"]
        self.assertIn("Not good", str(err.exception))

        with self.assertRaises(InvalidArgumentsError) as err:
            NDArray[Any, "Not a Shape Expression"]
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
            NDArray["Not a DType", Any]
        self.assertIn("Not a DType", str(err.exception))

    def test_valid_arguments_should_not_raise(self):
        NDArray
        NDArray[Any, Any]
        NDArray[Any, Shape["1"]]
        NDArray[(Any, Shape["1"])]
        NDArray[(Any, Literal["1"])]

    def test_str(self):
        self.assertEqual("NDArray[Any, Any]", str(NDArray[Any, Any]))
        self.assertEqual("NDArray[Any, Any]", str(NDArray[Any, Shape[" * , ... "]]))
        self.assertEqual(
            "NDArray[Any, Shape['2, 2']]", str(NDArray[Any, Shape[" 2 , 2 "]])
        )
        self.assertEqual("NDArray[UByte, Any]", str(NDArray[UInt8, Any]))
        self.assertEqual("NDArray[UByte, Any]", str(NDArray[np.uint8, Any]))
        self.assertEqual(
            str(NDArray[Any, Shape[" 2 , 2 "]]), repr(NDArray[Any, Shape[" 2 , 2 "]])
        )

    def test_types_with_numpy_dtypes(self):
        self.assertIsInstance(np.array([42]), NDArray[np.int_, Any])
        self.assertIsInstance(np.array([42.0]), NDArray[np.float_, Any])
        self.assertIsInstance(np.array([np.uint8(42)]), NDArray[np.uint8, Any])
        self.assertIsInstance(np.array([True]), NDArray[np.bool_, Any])

    def test_types_with_nptyping_aliases(self):
        self.assertIsInstance(np.array([42]), NDArray[Int, Any])
        self.assertIsInstance(np.array([42.0]), NDArray[Float, Any])
        self.assertIsInstance(np.array([np.uint8(42)]), NDArray[UInt8, Any])
        self.assertIsInstance(np.array([True]), NDArray[Bool, Any])

    def test_recursive_structure_is_forbidden(self):
        with self.assertRaises(NPTypingError) as err:
            NDArray[Int, Any][Int, Any]
        self.assertEqual(
            "Type NDArray[Int, Any] is already parameterized", str(err.exception)
        )

    def test_ndarray_is_hashable(self):
        hash(NDArray)
        hash(NDArray[Any, Any])
        hash(NDArray[Any, Shape["2, 2"]])

    def test_instantiation_is_forbidden(self):
        with self.assertRaises(NPTypingError):
            NDArray[Any, Shape["2, 2"]]()

    def test_subclassing_is_forbidden(self):
        with self.assertRaises(NPTypingError):

            class C(NDArray):
                ...

    def test_changing_attributes_is_forbidden(self):
        with self.assertRaises(NPTypingError):
            NDArray[Any, Any].__args__ = (1, 2)

        with self.assertRaises(NPTypingError):
            NDArray[Any, Any].some_attr = 42
