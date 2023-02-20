from unittest import TestCase

import numpy as np

from nptyping import Structure
from nptyping.error import InvalidStructureError
from nptyping.structure_expression import (
    check_structure,
    create_name_to_type_dict,
    normalize_structure_expression,
    validate_structure_expression,
)
from nptyping.typing_ import dtype_per_name


class StructureExpressionTest(TestCase):
    def test_check_structure_true(self):
        dtype = np.dtype([("name", "U10"), ("age", "i4")])
        structure = Structure["name: Str, age: Int32"]
        self.assertTrue(check_structure(dtype, structure, dtype_per_name))

        dtype2 = np.dtype([("a", "i4"), ("b", "i4"), ("c", "i8")])
        structure2 = Structure["[a, b, c]: Integer"]
        self.assertTrue(check_structure(dtype2, structure2, dtype_per_name))

        dtype3 = np.dtype([("a", "i4"), ("b", "i4"), ("c", "i8")])
        structure3 = Structure["[a, b, c]: Int"]
        self.assertTrue(check_structure(dtype3, structure3, dtype_per_name))

        dtype4 = np.dtype([("name", "U10")])
        structure4 = Structure["name: *"]
        self.assertTrue(check_structure(dtype4, structure4, dtype_per_name))

    def test_check_structure_with_sub_array(self):
        dtype = np.dtype([("x", "U10", (2, 2))])
        structure = Structure["x: Str[2, 2]"]
        self.assertTrue(check_structure(dtype, structure, dtype_per_name))

        dtype2 = np.dtype([("x", "U10", (2, 2))])
        structure2 = Structure["x: Int[2, 2]"]
        self.assertFalse(
            check_structure(dtype2, structure2, dtype_per_name),
            "It should fail because of the type.",
        )

        dtype3 = np.dtype([("x", "U10", (3, 3))])
        structure3 = Structure["x: Str[2, 2]"]
        self.assertFalse(
            check_structure(dtype3, structure3, dtype_per_name),
            "It should fail because of the shape.",
        )

        dtype4 = np.dtype([("x", "U10", (2, 2)), ("y", "U10", (2, 2))])
        structure4 = Structure["x: Str[2, 2], y: Str[2, 2]"]
        self.assertTrue(check_structure(dtype4, structure4, dtype_per_name))

        dtype5 = np.dtype([("x", "U10", (2, 2)), ("y", "U10", (2, 2))])
        structure5 = Structure["[x, y]: Str[2, 2]"]
        self.assertTrue(check_structure(dtype5, structure5, dtype_per_name))

        dtype6 = np.dtype([("x", "U10")])
        structure6 = Structure["x: Str[2, 2]"]
        self.assertFalse(
            check_structure(dtype6, structure6, dtype_per_name),
            "It should fail because it doesn't contain a sub array at all.",
        )

    def test_check_structure_false(self):
        dtype = np.dtype([("name", "U10"), ("age", "i4")])
        structure = Structure["name: Str, age: UInt"]
        self.assertFalse(check_structure(dtype, structure, dtype_per_name))

    def test_check_structure_invalid_type(self):
        dtype = np.dtype([("name", "U10"), ("age", "i4")])
        structure = Structure["name: Str, age: Ui"]
        with self.assertRaises(InvalidStructureError) as err:
            check_structure(dtype, structure, dtype_per_name)
        self.assertEqual(
            "Type 'Ui' is not valid in this context. Did you mean 'Unicode'?",
            str(err.exception),
        )

        dtype2 = np.dtype([("name", "U10"), ("age", "i4")])
        structure2 = Structure["name: Str, age: uint"]
        with self.assertRaises(InvalidStructureError) as err:
            check_structure(dtype2, structure2, dtype_per_name)
        self.assertEqual(
            "Type 'uint' is not valid in this context. Did you mean one of"
            " 'Int', 'UInt', 'IntP'?",
            str(err.exception),
        )

        dtype3 = np.dtype([("name", "U10"), ("age", "i4")])
        structure3 = Structure["name: Str, age: not_even_close"]
        with self.assertRaises(InvalidStructureError) as err:
            check_structure(dtype3, structure3, dtype_per_name)
        self.assertEqual(
            "Type 'not_even_close' is not valid in this context.", str(err.exception)
        )

    def test_check_structure_that_is_subset_or_superset_of_dtype(self):
        dtype1 = np.dtype([("x", "i4"), ("y", "i4")])
        structure1 = Structure["x: Int"]
        self.assertFalse(check_structure(dtype1, structure1, dtype_per_name))

        dtype2 = np.dtype([("x", "i4"), ("y", "i4")])
        structure2 = Structure["x: Int, y: Int, z: Int"]
        self.assertFalse(check_structure(dtype2, structure2, dtype_per_name))

    def test_validate_structure_expression_success(self):
        # validate_structure_expression("_: t")
        validate_structure_expression("a: t")
        validate_structure_expression("a: type")
        validate_structure_expression("a: Type")
        validate_structure_expression("a: t_")
        validate_structure_expression("a: t_123")
        validate_structure_expression("a_123: t")
        validate_structure_expression("abc: type")
        validate_structure_expression("abc: *")
        validate_structure_expression("abc: type[2, 2]")
        validate_structure_expression("abc: type [*, ...]")
        validate_structure_expression("abc: type, def: type")
        validate_structure_expression("abc: type[*, 2, ...], def: type[2 ]")
        validate_structure_expression("[abc, def]: type")
        validate_structure_expression("[abc, def]: type, *")
        validate_structure_expression("[abc, def]: type[*, ...]")
        validate_structure_expression("[abc, def]: type1, ghi: type2")
        validate_structure_expression("[abc, def]: type1, [ghi, jkl]: type2")
        validate_structure_expression(
            "[abc, def]: type1, [ghi, jkl]: type2, mno: type3"
        )
        validate_structure_expression("[abc,def]:type1,[ghi,jkl]:type2,mno:type3")
        validate_structure_expression(
            "  [  abc  ,  def  ]  :  type1  ,  [  ghi  ,  jkl  ]  :  type2  ,"
            "  mno  :  type3  "
        )

    def test_validate_structure_expression_fail(self):
        with self.assertRaises(InvalidStructureError):
            validate_structure_expression("a: _")
        with self.assertRaises(InvalidStructureError):
            validate_structure_expression("a: 1")
        with self.assertRaises(InvalidStructureError):
            validate_structure_expression("1: t")
        with self.assertRaises(InvalidStructureError):
            validate_structure_expression("abc: type$")
        with self.assertRaises(InvalidStructureError):
            validate_structure_expression("a$bc: type$")
        with self.assertRaises(InvalidStructureError):
            validate_structure_expression("ab c: type")
        with self.assertRaises(InvalidStructureError):
            validate_structure_expression("abc: type,")
        with self.assertRaises(InvalidStructureError):
            validate_structure_expression("abc:: type")
        with self.assertRaises(InvalidStructureError):
            validate_structure_expression("[a]: type")
        with self.assertRaises(InvalidStructureError):
            validate_structure_expression("[a,]: type")
        with self.assertRaises(InvalidStructureError):
            validate_structure_expression("[a,b,]: type")
        with self.assertRaises(InvalidStructureError):
            validate_structure_expression("[,a,b]: type")
        with self.assertRaises(InvalidStructureError):
            validate_structure_expression("abc: type []")
        with self.assertRaises(InvalidStructureError):
            validate_structure_expression("a: t[]")
        with self.assertRaises(InvalidStructureError) as err:
            validate_structure_expression(
                "a: t[*, 2, ...], b: t[not-a-valid-shape-expression]"
            )
        self.assertIn("not-a-valid-shape-expression", str(err.exception))
        with self.assertRaises(InvalidStructureError) as err:
            validate_structure_expression("a: t1, b: t2, c: t3, a: t4")
        self.assertEqual(
            "Field names may occur only once in a structure expression. Field"
            " name 'a' occurs 2 times in 'a: t1, b: t2, c: t3, a: t4'.",
            str(err.exception),
        )
        with self.assertRaises(InvalidStructureError) as err:
            validate_structure_expression("[a, b, c]: t1, [d, e, b]: t2, b: t3")
        self.assertEqual(
            "Field names may occur only once in a structure expression. Field"
            " name 'b' occurs 3 times in '[a, b, c]: t1, [d, e, b]: t2, b: t3'.",
            str(err.exception),
        )

    def test_normalize_structure_expression(self):
        self.assertEqual("a: t", normalize_structure_expression("  a  :  t  "))
        self.assertEqual("a: t", normalize_structure_expression("a:t"))
        self.assertEqual(
            "b: t1, [a, c]: t2", normalize_structure_expression("c: t2, b: t1, a: t2")
        )
        self.assertEqual(
            "[a, c]: *, b: t1", normalize_structure_expression("c: *, b: t1, a: *")
        )
        self.assertEqual(
            "b: t1, [a, c]: t2", normalize_structure_expression("[a, c]: t2, b: t1")
        )
        self.assertEqual(
            "[a, b, c]: t", normalize_structure_expression("[b, a]: t, c: t")
        )
        self.assertEqual(
            "[a, b, d, e]: t1, c: t2",
            normalize_structure_expression("[b, a]: t1, c: t2, [d, e]: t1"),
        )
        self.assertEqual(
            "a: t[*, ...]", normalize_structure_expression("  a  :  t  [ * , ... ]")
        )

    def test_create_name_to_type_dict(self):
        output = create_name_to_type_dict("a: t1, b: t2, c: t1")
        expected = {"a": "t1", "b": "t2", "c": "t1"}
        self.assertDictEqual(expected, output)

    def test_structure_depicting_at_least(self):
        # Test that you can define a Structure that expresses a structure with
        # at least some columns of some type.
        dtype_true1 = np.dtype([("a", "U10"), ("b", "i4")])
        dtype_true2 = np.dtype([("a", "U10"), ("b", "i4"), ("c", "i4"), ("d", "i4")])
        dtype_false1 = np.dtype([("a", "U10"), ("b", "U10")])
        dtype_false2 = np.dtype([("b", "i4"), ("c", "i4"), ("d", "i4")])

        structure = Structure["a: Str, b: Int32, *"]

        self.assertTrue(check_structure(dtype_true1, structure, dtype_per_name))
        self.assertTrue(check_structure(dtype_true2, structure, dtype_per_name))
        self.assertFalse(check_structure(dtype_false1, structure, dtype_per_name))
        self.assertFalse(check_structure(dtype_false2, structure, dtype_per_name))
