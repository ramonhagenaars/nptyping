from unittest import TestCase

from tests.test_helpers.check_mypy_on_code import check_mypy_on_code


class MyPyTest(TestCase):
    def test_mypy_accepts_ndarray_with_any(self):
        exit_code, stdout, stderr = check_mypy_on_code(
            """
            from typing import Any
            from nptyping import NDArray


            NDArray[Any, Any]
        """
        )
        self.assertEqual(0, exit_code, stdout)

    def test_mypy_accepts_ndarray_with_shape(self):
        exit_code, stdout, stderr = check_mypy_on_code(
            """
            from typing import Any
            from nptyping import NDArray, Shape


            NDArray[Shape["3, 3"], Any]
        """
        )

        self.assertEqual(0, exit_code, stdout)

    def test_mypy_accepts_ndarray_with_structure(self):
        exit_code, stdout, stderr = check_mypy_on_code(
            """
            from typing import Any
            from nptyping import NDArray, RecArray, Structure


            NDArray[Any, Structure["x: Float, y: Int"]]
        """
        )

        self.assertEqual(0, exit_code, stdout)

    def test_mypy_disapproves_ndarray_with_wrong_function_arguments(self):
        exit_code, stdout, stderr = check_mypy_on_code(
            """
            from typing import Any
            import numpy as np
            from nptyping import NDArray, Shape


            def func(_: NDArray[Shape["2, 2"], Any]) -> None:
                ...


            func("Not an array...")
        """
        )

        self.assertIn('Argument 1 to "func" has incompatible type "str"', stdout)
        self.assertIn('expected "ndarray[Any, Any]"', stdout)
        self.assertIn("Found 1 error in 1 file", stdout)

    def test_mypy_accepts_ndarrays_as_function_arguments(self):
        exit_code, stdout, stderr = check_mypy_on_code(
            """
            from typing import Any
            import numpy as np
            from nptyping import NDArray, Shape


            def func(_: NDArray[Shape["2, 2"], Any]) -> None:
                ...


            func(np.array([1, 2]))  # (Wrong shape though)
        """
        )

        self.assertEqual(0, exit_code, stdout)

    def test_mypy_accepts_ndarrays_as_variable_hints(self):
        exit_code, stdout, stderr = check_mypy_on_code(
            """
            from typing import Any
            import numpy as np
            from nptyping import NDArray


            arr: NDArray[Any, Any] = np.array([1, 2, 3])
        """
        )

        self.assertEqual(0, exit_code, stdout)

    def test_mypy_accepts_recarray_with_structure(self):
        exit_code, stdout, stderr = check_mypy_on_code(
            """
            from typing import Any
            from nptyping import RecArray, Structure


            RecArray[Any, Structure["x: Float, y: Int"]]
        """
        )

        self.assertEqual(0, exit_code, stdout)

    def test_mypy_accepts_numpy_types(self):
        exit_code, stdout, stderr = check_mypy_on_code(
            """
            from typing import Any
            from nptyping import NDArray
            import numpy as np


            NDArray[Any, np.dtype[np.int_]]
            NDArray[Any, np.dtype[np.float_]]
            NDArray[Any, np.dtype[np.uint8]]
            NDArray[Any, np.dtype[np.bool_]]
        """
        )

        self.assertEqual(0, exit_code, stdout)

    def test_mypy_wont_accept_numpy_types_without_dtype(self):
        exit_code, stdout, stderr = check_mypy_on_code(
            """
            from nptyping import NDArray
            from typing import Any
            import numpy as np


            NDArray[Any, np.int_]
        """
        )

        self.assertIn(
            'Value of type variable "_DType_co" of "ndarray" cannot be "signedinteger[Any]"',
            stdout,
        )

    def test_mypy_knows_of_ndarray_methods(self):
        # If MyPy knows of some arbitrary ndarray methods, we can assume that
        # code completion works.
        exit_code, stdout, stderr = check_mypy_on_code(
            """
            from typing import Any
            from nptyping import NDArray


            arr: NDArray[Any, Any]
            arr.shape
            arr.size
            arr.sort
            arr.squeeze
            arr.transpose
        """
        )

        self.assertEqual(0, exit_code, stdout)

    def test_mypy_accepts_nptyping_types(self):
        exit_code, stdout, stderr = check_mypy_on_code(
            """
            from typing import Any
            import numpy as np
            import numpy.typing as npt
            from nptyping import (
                NDArray,
                Number,
                Bool,
                Bool8,
                Object,
                Object0,
                Datetime64,
                Integer,
                SignedInteger,
                Int8,
                Int16,
                Int32,
                Int64,
                Byte,
                Short,
                IntC,
                IntP,
                Int0,
                Int,
                LongLong,
                Timedelta64,
                UnsignedInteger,
                UInt8,
                UInt16,
                UInt32,
                UInt64,
                UByte,
                UShort,
                UIntC,
                UIntP,
                UInt0,
                UInt,
                ULongLong,
                Inexact,
                Floating,
                Float16,
                Float32,
                Float64,
                Half,
                Single,
                Double,
                Float,
                LongDouble,
                LongFloat,
                ComplexFloating,
                Complex64,
                Complex128,
                CSingle,
                SingleComplex,
                CDouble,
                Complex,
                CFloat,
                CLongDouble,
                CLongFloat,
                LongComplex,
                Flexible,
                Void,
                Void0,
                Character,
                Bytes,
                String,
                Bytes0,
                Unicode,
                Str0,
            )

            NDArray[Any, Number]
            NDArray[Any, Bool]
            NDArray[Any, Bool8]
            NDArray[Any, Object]
            NDArray[Any, Object0]
            NDArray[Any, Datetime64]
            NDArray[Any, Integer]
            NDArray[Any, SignedInteger]
            NDArray[Any, Int8]
            NDArray[Any, Int16]
            NDArray[Any, Int32]
            NDArray[Any, Int64]
            NDArray[Any, Byte]
            NDArray[Any, Short]
            NDArray[Any, IntC]
            NDArray[Any, IntP]
            NDArray[Any, Int0]
            NDArray[Any, Int]
            NDArray[Any, LongLong]
            NDArray[Any, Timedelta64]
            NDArray[Any, UnsignedInteger]
            NDArray[Any, UInt8]
            NDArray[Any, UInt16]
            NDArray[Any, UInt32]
            NDArray[Any, UInt64]
            NDArray[Any, UByte]
            NDArray[Any, UShort]
            NDArray[Any, UIntC]
            NDArray[Any, UIntP]
            NDArray[Any, UInt0]
            NDArray[Any, UInt]
            NDArray[Any, ULongLong]
            NDArray[Any, Inexact]
            NDArray[Any, Floating]
            NDArray[Any, Float16]
            NDArray[Any, Float32]
            NDArray[Any, Float64]
            NDArray[Any, Half]
            NDArray[Any, Single]
            NDArray[Any, Double]
            NDArray[Any, Float]
            NDArray[Any, LongDouble]
            NDArray[Any, LongFloat]
            NDArray[Any, ComplexFloating]
            NDArray[Any, Complex64]
            NDArray[Any, Complex128]
            NDArray[Any, CSingle]
            NDArray[Any, SingleComplex]
            NDArray[Any, CDouble]
            NDArray[Any, Complex]
            NDArray[Any, CFloat]
            NDArray[Any, CLongDouble]
            NDArray[Any, CLongFloat]
            NDArray[Any, LongComplex]
            NDArray[Any, Flexible]
            NDArray[Any, Void]
            NDArray[Any, Void0]
            NDArray[Any, Character]
            NDArray[Any, Bytes]
            NDArray[Any, String]
            NDArray[Any, Bytes0]
            NDArray[Any, Unicode]
            NDArray[Any, Str0]
        """
        )

        self.assertEqual(0, exit_code, stdout)
