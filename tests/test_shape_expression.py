from unittest import TestCase

from nptyping import (
    InvalidShapeError,
    normalize_shape_expression,
    validate_shape_expression,
)


class ShapeExpressionTest(TestCase):
    def test_validate_shape_expression_success(self):
        validate_shape_expression("1")
        validate_shape_expression("1, 2")
        validate_shape_expression("1, 2, 3")
        validate_shape_expression("1, ...")
        validate_shape_expression("*, ...")
        validate_shape_expression("*, *, ...")
        validate_shape_expression("VaRiAbLe123, ...")
        validate_shape_expression("[a, b], ...")
        validate_shape_expression("2, 3, ...")
        validate_shape_expression("*, *, *")
        validate_shape_expression("VaRiAbLe123, VaRiAbLe123, VaRiAbLe123")
        validate_shape_expression("[a]")
        validate_shape_expression("[a, b]")
        validate_shape_expression("[a, b], [c]")
        validate_shape_expression("[a, b], [c], 1")
        validate_shape_expression("1 stuff")
        validate_shape_expression("1 value of stuff")
        validate_shape_expression("1 stuff, 2 stuff")
        validate_shape_expression("[a, b, c] stuff")
        validate_shape_expression("  [  a  ,  b  ,  c  ]  stuff  ")
        validate_shape_expression(
            "  [  a  ,  b  ,  c  ]  stuff, *, VaRiAbLe123, 2 stuff"
        )
        validate_shape_expression("[a,b,c] stuff,*,VaRiAbLe123,2 stuff")

    def test_validate_shape_expression_fail(self):
        with self.assertRaises(InvalidShapeError):
            validate_shape_expression("")
        with self.assertRaises(InvalidShapeError):
            validate_shape_expression("   ")
        with self.assertRaises(InvalidShapeError):
            validate_shape_expression("just_a_label")
        with self.assertRaises(InvalidShapeError):
            validate_shape_expression("1number_with_a_label_attached")
        with self.assertRaises(InvalidShapeError):
            validate_shape_expression("_")
        with self.assertRaises(InvalidShapeError):
            validate_shape_expression("1, [2, 2]")
        with self.assertRaises(InvalidShapeError):
            validate_shape_expression("1, [NoVars, InDimBreakdowns]")
        with self.assertRaises(InvalidShapeError):
            validate_shape_expression("1, ..., 2")
        with self.assertRaises(InvalidShapeError):
            validate_shape_expression("**")
        with self.assertRaises(InvalidShapeError):
            validate_shape_expression("1,")
        with self.assertRaises(InvalidShapeError):
            validate_shape_expression("[a,]")
        with self.assertRaises(InvalidShapeError):
            validate_shape_expression("1 label with a number 2")

    def test_normalize_shape_expression(self):
        self.assertEqual("1, 1", normalize_shape_expression(" 1 , 1 "))
        self.assertEqual("X, Y", normalize_shape_expression(" X , Y "))
        self.assertEqual("1, ...", normalize_shape_expression(" 1 , ... "))
        self.assertEqual(
            "1, [a, b], C", normalize_shape_expression(" 1 , [ a , b ] , C ")
        )
        self.assertEqual(
            "1 label1 label2", normalize_shape_expression(" 1  label1  label2 ")
        )
        self.assertEqual(
            "1 label1 label2, [label3, label4]",
            normalize_shape_expression(" 1  label1  label2 ,  [ label3 , label4 ] "),
        )
