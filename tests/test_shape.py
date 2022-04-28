from unittest import TestCase

from nptyping import Shape
from nptyping.error import InvalidArgumentsError
from nptyping.typing_ import Literal


class ShapeTest(TestCase):
    def test_happy_flow(self):
        self.assertIs(Shape["2, 2"], Shape["2, 2 "])

    def test_invalid_argument_is_detected(self):
        with self.assertRaises(InvalidArgumentsError) as err:
            Shape[42]

        self.assertIn("int", str(err.exception))
        self.assertIn("str", str(err.exception))

    def test_str(self):
        self.assertEqual("Shape['2, 2']", str(Shape[" 2 , 2 "]))

    def test_repr(self):
        self.assertEqual("Shape['2, 2']", repr(Shape[" 2 , 2 "]))

    def test_shape_and_literal_are_interchangeable(self):
        self.assertEqual(Shape["2, 2"], Literal["2, 2"])
