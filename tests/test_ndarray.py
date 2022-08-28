from typing import Any
from unittest import TestCase

import numpy as np

from nptyping import (
    Bool,
    Float,
    Int,
    InvalidArgumentsError,
    InvalidStructureError,
    NDArray,
    NPTypingError,
    Shape,
    Structure,
    UInt8,
)
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

    def test_isinstance_fails_if_shape_size_dont_match(self):
        self.assertNotIsInstance(
            np.random.randn(2, 2),
            NDArray[Shape["2, 3"], Any],
        )

    def test_isinstance_fails_if_nr_of_shapes_dont_match(self):
        self.assertNotIsInstance(
            np.random.randn(2, 2),
            NDArray[Shape["2, 2, 2"], Any],
        )
        self.assertNotIsInstance(
            np.random.randn(2, 2),
            NDArray[Shape["2"], Any],
        )

    def test_isinstance_succeeds_if_variables_can_be_assigned(self):
        self.assertIsInstance(
            np.random.randn(3, 2),
            NDArray[Shape["Axis1, Axis2"], Any],
        )
        self.assertIsInstance(
            np.random.randn(3, 2),
            NDArray[Shape["Axis, 2"], Any],
            "Combinations of variables and values should work.",
        )
        self.assertIsInstance(
            np.random.randn(2),
            NDArray[Shape["VaR14bLe_"], Any],
            "Anything that starts with an uppercase letter is a variable.",
        )

    def test_isinstance_fails_if_variables_cannot_be_assigned(self):
        self.assertNotIsInstance(
            np.random.randn(3, 2),
            NDArray[Shape["Axis1, Axis1"], Any],
        )

    def test_isinstance_succeeds_with_wildcards(self):
        self.assertIsInstance(
            np.random.randn(4),
            NDArray[Shape["*"], Any],
        )
        self.assertIsInstance(
            np.random.randn(4, 4),
            NDArray[Shape["*, *"], Any],
        )

    def test_isinstance_succeeds_with_0d_arrays(self):
        self.assertIsInstance(
            np.array([]),
            NDArray[Shape["0"], Any],
        )

    def test_isinstance_succeeds_with_ellipsis(self):
        self.assertIsInstance(
            np.array([[[[[[0]]]]]]),
            NDArray[Shape["1, ..."], Any],
            "This should match with an array of any dimensions of size 1.",
        )
        self.assertIsInstance(
            np.array([[[[[[0, 0, 0]]]]]]),
            NDArray[Shape["*, ..."], Any],
            "This should match with an array of any dimensions of any size.",
        )
        self.assertIsInstance(
            np.array([[0]]),
            NDArray[Shape["1, 1, ..."], Any],
            "This should match with an array of shape (1, 1).",
        )
        self.assertIsInstance(
            np.array([[[[0]]]]),
            NDArray[Shape["1, 1, ..."], Any],
            "This should match with an array of shape (1, 1, 1, 1).",
        )
        self.assertIsInstance(
            np.array([[[[0, 0], [0, 0]], [[0, 0], [0, 0]]]]),
            NDArray[Shape["1, 2, ..."], Any],
        )

    def test_isinstance_fails_with_ellipsis(self):
        self.assertNotIsInstance(
            np.array([[[[[[0, 0]]]]]]),
            NDArray[Shape["1, ..."], Any],
            "This should match with an array of any dimensions of size 1.",
        )
        self.assertNotIsInstance(
            np.array([[[[[0], [0]], [[0], [0]]], [[[0], [0]], [[0], [0]]]]]),
            NDArray[Shape["1, 2, ..."], Any],
        )

    def test_isinstance_succeeds_with_dim_breakdown(self):
        self.assertIsInstance(
            np.random.randn(3, 2),
            NDArray[Shape["3, [x, y]"], Any],
        )
        self.assertIsInstance(
            np.random.randn(3, 2),
            NDArray[Shape["[obj1, obj2, obj3], [x, y]"], Any],
        )

    def test_isinstance_fails_with_dim_breakdown(self):
        self.assertNotIsInstance(
            np.random.randn(3, 2),
            NDArray[Shape["3, [x, y, z]"], Any],
        )

    def test_isinstance_succeeds_with_labels(self):
        self.assertIsInstance(
            np.random.randn(100, 5),
            NDArray[Shape["100 assets, [id, age, type, x, y]"], Any],
        )
        self.assertIsInstance(
            np.random.randn(100, 5),
            NDArray[Shape["* assets, [id, age, type, x, y]"], Any],
        )
        self.assertIsInstance(
            np.random.randn(100, 5),
            NDArray[Shape["N assets, [id, age, type, x, y]"], Any],
        )

    def test_isinstance_succeeds_if_structure_match_exactly(self):
        arr = np.array([("Pete", 34)], dtype=[("name", "U8"), ("age", "i4")])
        self.assertIsInstance(
            arr,
            NDArray[Any, Structure["name: Str, age: Int32"]],
        )

    def test_isinstance_fails_if_structure_doesnt_match(self):
        arr = np.array([("Johnny", 34)], dtype=[("name", "U8"), ("age", "i4")])
        self.assertNotIsInstance(
            arr,
            NDArray[Any, Structure["name: Str, age: Float"]],
        )

        arr = np.array([("Bill", 34)], dtype=[("name", "U8"), ("age", "i4")])
        self.assertNotIsInstance(
            arr,
            NDArray[Any, Structure["name: String, age: Int32"]],
        )

        arr = np.array([("Clair", 34)], dtype=[("name", "U8"), ("age", "i4")])
        self.assertNotIsInstance(
            arr,
            NDArray[Any, Structure["[name, age]: Str"]],
        )

    def test_isinstance_succeeds_if_structure_subarray_matches(self):
        arr = np.array([("x")], np.dtype([("x", "U10", (2, 2))]))
        self.assertIsInstance(arr, NDArray[Any, Structure["x: Str[2, 2]"]])

    def test_isinstance_fails_if_structure_contains_invalid_types(self):
        with self.assertRaises(InvalidStructureError) as err:
            NDArray[Any, Structure["name: Str, age: Float, address: Address"]]
        self.assertIn(
            "Type 'Address' is not valid in this context.", str(err.exception)
        )

        with self.assertRaises(InvalidStructureError) as err:
            NDArray[Any, Literal["x: Float, y: AlsoAFloat"]]
        self.assertIn(
            "Type 'AlsoAFloat' is not valid in this context.", str(err.exception)
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

        with self.assertRaises(InvalidArgumentsError) as err:
            NDArray[Any, "Not a DType"]
        self.assertIn("Not a DType", str(err.exception))

    def test_valid_arguments_should_not_raise(self):
        NDArray
        NDArray[Any, Any]
        NDArray[Shape["1"], Any]
        NDArray[(Shape["1"], Any)]
        NDArray[Literal["1"], Any]
        NDArray[Any, Int]
        NDArray[Any, Structure["x: Float"]]
        NDArray[Any, Structure["x: Float, y: Int"]]
        NDArray[Any, Structure["[x, y]: Float, z: Int"]]
        NDArray[Any, Literal["[x, y]: Float, z: Int"]]

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
        self.assertEqual(
            "NDArray[Any, Structure['[x, y]: Float']]",
            str(NDArray[Any, Structure["x: Float, y: Float"]]),
        )
        self.assertEqual(
            "NDArray[Any, Structure['[x, y]: Float']]",
            repr(NDArray[Any, Structure["x: Float, y: Float"]]),
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
            "Type nptyping.NDArray[Any, Int] is already parameterized.",
            str(err.exception),
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

            class SomeSubclass(NDArray):
                ...

    def test_changing_attributes_is_forbidden(self):
        with self.assertRaises(NPTypingError):
            NDArray[Any, Any].__args__ = (1, 2)

        with self.assertRaises(NPTypingError):
            NDArray[Any, Any].some_attr = 42
