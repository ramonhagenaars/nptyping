"""
MIT License

Copyright (c) 2022 Ramon Hagenaars

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from nptyping.assert_isinstance import assert_isinstance  # type: ignore[attr-defined]
from nptyping.error import (
    InvalidArgumentsError,
    InvalidShapeError,
    NPTypingError,
)
from nptyping.ndarray import NDArray
from nptyping.package_info import __version__
from nptyping.shape_expression import (
    normalize_shape_expression,
    validate_shape_expression,
)
from nptyping.typing_ import (  # type: ignore[attr-defined]
    Bool,
    Bool8,
    Byte,
    Bytes,
    Bytes0,
    CDouble,
    CFloat,
    Character,
    CLongDouble,
    CLongFloat,
    Complex,
    Complex64,
    Complex128,
    ComplexFloating,
    CSingle,
    Datetime64,
    Double,
    DType,
    Flexible,
    Float,
    Float16,
    Float32,
    Float64,
    Floating,
    Half,
    Inexact,
    Int,
    Int0,
    Int8,
    Int16,
    Int32,
    Int64,
    IntC,
    Integer,
    IntP,
)
from nptyping.typing_ import Literal as Shape  # type: ignore[attr-defined]
from nptyping.typing_ import (  # type: ignore[attr-defined]
    LongComplex,
    LongDouble,
    LongFloat,
    LongLong,
    Number,
    Object,
    Object0,
    Short,
    SignedInteger,
    Single,
    SingleComplex,
    Str0,
    String,
    Timedelta64,
    UByte,
    UInt,
    UInt0,
    UInt8,
    UInt16,
    UInt32,
    UInt64,
    UIntC,
    UIntP,
    ULongLong,
    Unicode,
    UnsignedInteger,
    UShort,
    Void,
    Void0,
)

__all__ = [
    "NDArray",
    "assert_isinstance",
    "validate_shape_expression",
    "normalize_shape_expression",
    "NPTypingError",
    "InvalidShapeError",
    "InvalidArgumentsError",
    "Shape",
    "__version__",
    "DType",
    "Number",
    "Bool",
    "Bool8",
    "Object",
    "Object0",
    "Datetime64",
    "Integer",
    "SignedInteger",
    "Int8",
    "Int16",
    "Int32",
    "Int64",
    "Byte",
    "Short",
    "IntC",
    "IntP",
    "Int0",
    "Int",
    "LongLong",
    "Timedelta64",
    "UnsignedInteger",
    "UInt8",
    "UInt16",
    "UInt32",
    "UInt64",
    "UByte",
    "UShort",
    "UIntC",
    "UIntP",
    "UInt0",
    "UInt",
    "ULongLong",
    "Inexact",
    "Floating",
    "Float16",
    "Float32",
    "Float64",
    "Half",
    "Single",
    "Double",
    "Float",
    "LongDouble",
    "LongFloat",
    "ComplexFloating",
    "Complex64",
    "Complex128",
    "CSingle",
    "SingleComplex",
    "CDouble",
    "Complex",
    "CFloat",
    "CLongDouble",
    "CLongFloat",
    "LongComplex",
    "Flexible",
    "Void",
    "Void0",
    "Character",
    "Bytes",
    "String",
    "Bytes0",
    "Unicode",
    "Str0",
]
