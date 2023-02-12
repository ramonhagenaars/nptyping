"""
MIT License

Copyright (c) 2023 Ramon Hagenaars

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

try:
    from typing import (  # type: ignore[attr-defined,misc] # pylint: disable=unused-import
        Literal,
        TypeAlias,
        TypeGuard,
        final,
    )
except ImportError:  # pragma: no cover
    from typing_extensions import (  # type: ignore[attr-defined,misc]
        Literal,
        TypeAlias,
        TypeGuard,
        final,
    )

from typing import Tuple, Union

import numpy as np

ShapeExpression: TypeAlias = str
StructureExpression: TypeAlias = str
DType: TypeAlias = Union[np.generic, StructureExpression]
ShapeTuple: TypeAlias = Tuple[int, ...]

Number = np.number
Bool = np.bool_
Bool8 = np.bool8
Obj = np.object_  # Obj is a common abbreviation and should be usable.
Object = np.object_
Object0 = np.object0
Datetime64 = np.datetime64
Integer = np.integer
SignedInteger = np.signedinteger
Int8 = np.int8
Int16 = np.int16
Int32 = np.int32
Int64 = np.int64
Byte = np.byte
Short = np.short
IntC = np.intc
IntP = np.intp
Int0 = np.int0
Int = np.integer  # Int should translate to the "generic" int type.
Int_ = np.int_
LongLong = np.longlong
Timedelta64 = np.timedelta64
UnsignedInteger = np.unsignedinteger
UInt8 = np.uint8
UInt16 = np.uint16
UInt32 = np.uint32
UInt64 = np.uint64
UByte = np.ubyte
UShort = np.ushort
UIntC = np.uintc
UIntP = np.uintp
UInt0 = np.uint0
UInt = np.uint
ULongLong = np.ulonglong
Inexact = np.inexact
Floating = np.floating
Float16 = np.float16
Float32 = np.float32
Float64 = np.float64
Half = np.half
Single = np.single
Double = np.double
Float = np.float_
LongDouble = np.longdouble
LongFloat = np.longfloat
ComplexFloating = np.complexfloating
Complex64 = np.complex64
Complex128 = np.complex128
CSingle = np.csingle
SingleComplex = np.singlecomplex
CDouble = np.cdouble
Complex = np.complex_
CFloat = np.cfloat
CLongDouble = np.clongdouble
CLongFloat = np.clongfloat
LongComplex = np.longcomplex
Flexible = np.flexible
Void = np.void
Void0 = np.void0
Character = np.character
Bytes = np.bytes_
Str = np.str_
String = np.string_
Bytes0 = np.bytes0
Unicode = np.unicode_
Str0 = np.str0

dtypes = [
    (Number, "Number"),
    (Bool, "Bool"),
    (Bool8, "Bool8"),
    (Obj, "Obj"),
    (Object, "Object"),
    (Object0, "Object0"),
    (Datetime64, "Datetime64"),
    (Integer, "Integer"),
    (SignedInteger, "SignedInteger"),
    (Int8, "Int8"),
    (Int16, "Int16"),
    (Int32, "Int32"),
    (Int64, "Int64"),
    (Byte, "Byte"),
    (Short, "Short"),
    (IntC, "IntC"),
    (IntP, "IntP"),
    (Int0, "Int0"),
    (Int, "Int"),
    (LongLong, "LongLong"),
    (Timedelta64, "Timedelta64"),
    (UnsignedInteger, "UnsignedInteger"),
    (UInt8, "UInt8"),
    (UInt16, "UInt16"),
    (UInt32, "UInt32"),
    (UInt64, "UInt64"),
    (UByte, "UByte"),
    (UShort, "UShort"),
    (UIntC, "UIntC"),
    (UIntP, "UIntP"),
    (UInt0, "UInt0"),
    (UInt, "UInt"),
    (ULongLong, "ULongLong"),
    (Inexact, "Inexact"),
    (Floating, "Floating"),
    (Float16, "Float16"),
    (Float32, "Float32"),
    (Float64, "Float64"),
    (Half, "Half"),
    (Single, "Single"),
    (Double, "Double"),
    (Float, "Float"),
    (LongDouble, "LongDouble"),
    (LongFloat, "LongFloat"),
    (ComplexFloating, "ComplexFloating"),
    (Complex64, "Complex64"),
    (Complex128, "Complex128"),
    (CSingle, "CSingle"),
    (SingleComplex, "SingleComplex"),
    (CDouble, "CDouble"),
    (Complex, "Complex"),
    (CFloat, "CFloat"),
    (CLongDouble, "CLongDouble"),
    (CLongFloat, "CLongFloat"),
    (LongComplex, "LongComplex"),
    (Flexible, "Flexible"),
    (Void, "Void"),
    (Void0, "Void0"),
    (Character, "Character"),
    (Bytes, "Bytes"),
    (String, "String"),
    (Str, "Str"),
    (Bytes0, "Bytes0"),
    (Unicode, "Unicode"),
    (Str0, "Str0"),
]

name_per_dtype = dict(dtypes)
dtype_per_name = {name: dtype for dtype, name in dtypes}
