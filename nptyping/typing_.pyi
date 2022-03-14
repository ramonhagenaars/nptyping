# type: ignore
# Let MyPy ignore this file to avoid complaints on the imports of Literal and
# TypeAlias under different Python versions.
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
from typing import (
    Any,
    Dict,
    List,
    Tuple,
)

import numpy as np

try:
    from typing import (
        Literal,
        TypeAlias,
        final,
    )
except ImportError:
    from typing_extensions import (
        Literal,
        TypeAlias,
        final,
    )

def validate_dtype(dtype: Any) -> None: ...

DType: TypeAlias = Any
ShapeExpression: TypeAlias = Any

Number: TypeAlias = np.number
Bool: TypeAlias = np.bool_
Bool8: TypeAlias = np.bool8
Object: TypeAlias = np.object_
Object0: TypeAlias = np.object0
Datetime64: TypeAlias = np.datetime64
Integer: TypeAlias = np.integer
SignedInteger: TypeAlias = np.signedinteger
Int8: TypeAlias = np.int8
Int16: TypeAlias = np.int16
Int32: TypeAlias = np.int32
Int64: TypeAlias = np.int64
Byte: TypeAlias = np.byte
Short: TypeAlias = np.short
IntC: TypeAlias = np.intc
IntP: TypeAlias = np.intp
Int0: TypeAlias = np.int0
Int: TypeAlias = np.int_
LongLong: TypeAlias = np.longlong
Timedelta64: TypeAlias = np.timedelta64
UnsignedInteger: TypeAlias = np.unsignedinteger
UInt8: TypeAlias = np.uint8
UInt16: TypeAlias = np.uint16
UInt32: TypeAlias = np.uint32
UInt64: TypeAlias = np.uint64
UByte: TypeAlias = np.ubyte
UShort: TypeAlias = np.ushort
UIntC: TypeAlias = np.uintc
UIntP: TypeAlias = np.uintp
UInt0: TypeAlias = np.uint0
UInt: TypeAlias = np.uint
ULongLong: TypeAlias = np.ulonglong
Inexact: TypeAlias = np.inexact
Floating: TypeAlias = np.floating
Float16: TypeAlias = np.float16
Float32: TypeAlias = np.float32
Float64: TypeAlias = np.float64
Half: TypeAlias = np.half
Single: TypeAlias = np.single
Double: TypeAlias = np.double
Float: TypeAlias = np.float_
LongDouble: TypeAlias = np.longdouble
LongFloat: TypeAlias = np.longfloat
ComplexFloating: TypeAlias = np.complexfloating
Complex64: TypeAlias = np.complex64
Complex128: TypeAlias = np.complex128
CSingle: TypeAlias = np.csingle
SingleComplex: TypeAlias = np.singlecomplex
CDouble: TypeAlias = np.cdouble
Complex: TypeAlias = np.complex_
CFloat: TypeAlias = np.cfloat
CLongDouble: TypeAlias = np.clongdouble
CLongFloat: TypeAlias = np.clongfloat
LongComplex: TypeAlias = np.longcomplex
Flexible: TypeAlias = np.flexible
Void: TypeAlias = np.void
Void0: TypeAlias = np.void0
Character: TypeAlias = np.character
Bytes: TypeAlias = np.bytes_
String: TypeAlias = np.string_
Bytes0: TypeAlias = np.bytes0
Unicode: TypeAlias = np.unicode_
Str0: TypeAlias = np.str0

dtypes = List[Tuple[np.generic, str]]
name_per_dtype: Dict[np.generic, str]
