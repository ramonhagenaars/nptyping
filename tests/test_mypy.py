import os
from pathlib import Path
from tempfile import TemporaryDirectory
from textwrap import dedent
from unittest import TestCase

from mypy import api


def _check_mypy_on_code(python_code: str) -> str:
    file_content = dedent(python_code).strip() + os.linesep
    with TemporaryDirectory() as directory_name:
        path_to_file = Path(directory_name) / "mypy_test.py"
        with open(path_to_file, "w") as file:
            file.write(file_content)
        mypy_findings, _, _ = api.run([str(path_to_file)])
    return mypy_findings


class MyPyTest(TestCase):
    def test_mypy_accepts_any(self):
        mypy_findings = _check_mypy_on_code(
            """
            from typing import Any
            from nptyping import NDArray
            
            
            NDArray[Any, Any]
        """
        )

        self.assertIn("Success", mypy_findings)

    def test_mypy_accepts_shape(self):
        mypy_findings = _check_mypy_on_code(
            """
            from typing import Any
            from nptyping import NDArray, Shape
            
            
            NDArray[Any, Shape["3, 3"]]
        """
        )

        self.assertIn("Success", mypy_findings)

    def test_mypy_disapproves_wrong_function_arguments(self):
        mypy_findings = _check_mypy_on_code(
            """
            from typing import Any
            import numpy as np
            from nptyping import NDArray, Shape
            
            
            def func(_: NDArray[Any, Shape["2, 2"]]) -> None:
                ...
            

            func("Not an array...")            
        """
        )

        self.assertIn('Argument 1 to "func" has incompatible type "str"', mypy_findings)
        self.assertIn('expected "NDArray[Any, Any]"', mypy_findings)
        self.assertIn("Found 1 error in 1 file", mypy_findings)

    def test_mypy_accepts_ndarrays_as_function_arguments(self):
        mypy_findings = _check_mypy_on_code(
            """
            from typing import Any
            import numpy as np
            from nptyping import NDArray, Shape
            
            
            def func(_: NDArray[Any, Shape["2, 2"]]) -> None:
                ...
            
            
            func(np.array([1, 2]))  # (Wrong shape though)
        """
        )

        self.assertIn("Success", mypy_findings)

    def test_mypy_accepts_ndarrays_as_variable_hints(self):
        mypy_findings = _check_mypy_on_code(
            """
            from typing import Any
            import numpy as np
            from nptyping import NDArray
            
            
            arr: NDArray[Any, Any] = np.array([1, 2, 3])
        """
        )

        self.assertIn("Success", mypy_findings)

    def test_mypy_accepts_numpy_types(self):
        mypy_findings = _check_mypy_on_code(
            """
            from typing import Any
            from nptyping import NDArray
            import numpy as np
            
            
            NDArray[np.int_, Any]
            NDArray[np.float_, Any]
            NDArray[np.uint8, Any]
            NDArray[np.bool_, Any]
        """
        )

        self.assertIn("Success", mypy_findings)

    def test_mypy_accepts_nptyping_types(self):
        mypy_findings = _check_mypy_on_code(
            """
            from typing import Any
            import numpy as np
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
            
            NDArray[Number, Any]
            NDArray[Bool, Any]
            NDArray[Bool8, Any]
            NDArray[Object, Any]
            NDArray[Object0, Any]
            NDArray[Datetime64, Any]
            NDArray[Integer, Any]
            NDArray[SignedInteger, Any]
            NDArray[Int8, Any]
            NDArray[Int16, Any]
            NDArray[Int32, Any]
            NDArray[Int64, Any]
            NDArray[Byte, Any]
            NDArray[Short, Any]
            NDArray[IntC, Any]
            NDArray[IntP, Any]
            NDArray[Int0, Any]
            NDArray[Int, Any]
            NDArray[LongLong, Any]
            NDArray[Timedelta64, Any]
            NDArray[UnsignedInteger, Any]
            NDArray[UInt8, Any]
            NDArray[UInt16, Any]
            NDArray[UInt32, Any]
            NDArray[UInt64, Any]
            NDArray[UByte, Any]
            NDArray[UShort, Any]
            NDArray[UIntC, Any]
            NDArray[UIntP, Any]
            NDArray[UInt0, Any]
            NDArray[UInt, Any]
            NDArray[ULongLong, Any]
            NDArray[Inexact, Any]
            NDArray[Floating, Any]
            NDArray[Float16, Any]
            NDArray[Float32, Any]
            NDArray[Float64, Any]
            NDArray[Half, Any]
            NDArray[Single, Any]
            NDArray[Double, Any]
            NDArray[Float, Any]
            NDArray[LongDouble, Any]
            NDArray[LongFloat, Any]
            NDArray[ComplexFloating, Any]
            NDArray[Complex64, Any]
            NDArray[Complex128, Any]
            NDArray[CSingle, Any]
            NDArray[SingleComplex, Any]
            NDArray[CDouble, Any]
            NDArray[Complex, Any]
            NDArray[CFloat, Any]
            NDArray[CLongDouble, Any]
            NDArray[CLongFloat, Any]
            NDArray[LongComplex, Any]
            NDArray[Flexible, Any]
            NDArray[Void, Any]
            NDArray[Void0, Any]
            NDArray[Character, Any]
            NDArray[Bytes, Any]
            NDArray[String, Any]
            NDArray[Bytes0, Any]
            NDArray[Unicode, Any]
            NDArray[Str0, Any]
        """
        )

        self.assertIn("Success", mypy_findings)
