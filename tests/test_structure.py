from unittest import TestCase

from nptyping import Structure
from nptyping.error import InvalidArgumentsError
from nptyping.typing_ import Literal


class StructureTest(TestCase):
    def test_happy_flow(self):
        self.assertIs(Structure["name: type"], Structure["name: type "])

    def test_invalid_argument_is_detected(self):
        with self.assertRaises(InvalidArgumentsError) as err:
            Structure[42]

        self.assertIn("int", str(err.exception))
        self.assertIn("str", str(err.exception))

    def test_str(self):
        self.assertEqual("Structure['name: type']", str(Structure[" name : type "]))

    def test_repr(self):
        self.assertEqual("Structure['name: type']", repr(Structure[" name : type "]))

    def test_shape_and_literal_are_interchangeable(self):
        self.assertEqual(Structure["name: type"], Literal["name: type"])

    def test_get_types(self):
        structure = Structure["a: Float, b: Int, [c, d, e]: Complex"]
        self.assertEqual({"Float", "Int", "Complex"}, set(structure.get_types()))

    def test_get_names(self):
        structure = Structure["a: Float, b: Int, [c, d, e]: Complex"]
        self.assertEqual({"a", "b", "c", "d", "e"}, set(structure.get_names()))

    def test_structure_can_be_compared_to_literal(self):
        self.assertEqual(Structure["a: Int, b: Float"], Literal["a: Int, b: Float"])
        self.assertEqual(
            Structure["b: Float, a: Int"], Literal[" a : Int , b : Float "]
        )
