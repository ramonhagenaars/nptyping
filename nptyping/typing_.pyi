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
    from typing import (  # type: ignore[attr-defined] # pylint: disable=unused-import
        Dict,
        TypeAlias,
    )
except ImportError:  # pragma: no cover
    from typing_extensions import (
        TypeAlias,
    )

from typing import (
    Any,
    Tuple,
    Union,
)

import numpy as np

ShapeExpression: TypeAlias = str
StructureExpression: TypeAlias = str
DType: TypeAlias = Union[np.generic, StructureExpression]
ShapeTuple: TypeAlias = Tuple[int, ...]

Number: TypeAlias = np.dtype[np.number[Any]]
Bool: TypeAlias = np.dtype[np.bool_]
Bool8: TypeAlias = np.dtype[np.bool8]
Object: TypeAlias = np.dtype[np.object_]
Object0: TypeAlias = np.dtype[np.object0]
Datetime64: TypeAlias = np.dtype[np.datetime64]
Integer: TypeAlias = np.dtype[np.integer[Any]]
SignedInteger: TypeAlias = np.dtype[np.signedinteger[Any]]
Int8: TypeAlias = np.dtype[np.int8]
Int16: TypeAlias = np.dtype[np.int16]
Int32: TypeAlias = np.dtype[np.int32]
Int64: TypeAlias = np.dtype[np.int64]
Byte: TypeAlias = np.dtype[np.byte]
Short: TypeAlias = np.dtype[np.short]
IntC: TypeAlias = np.dtype[np.intc]
IntP: TypeAlias = np.dtype[np.intp]
Int0: TypeAlias = np.dtype[np.int0]
Int: TypeAlias = np.dtype[np.int_]
LongLong: TypeAlias = np.dtype[np.longlong]
Timedelta64: TypeAlias = np.dtype[np.timedelta64]
UnsignedInteger: TypeAlias = np.dtype[np.unsignedinteger[Any]]
UInt8: TypeAlias = np.dtype[np.uint8]
UInt16: TypeAlias = np.dtype[np.uint16]
UInt32: TypeAlias = np.dtype[np.uint32]
UInt64: TypeAlias = np.dtype[np.uint64]
UByte: TypeAlias = np.dtype[np.ubyte]
UShort: TypeAlias = np.dtype[np.ushort]
UIntC: TypeAlias = np.dtype[np.uintc]
UIntP: TypeAlias = np.dtype[np.uintp]
UInt0: TypeAlias = np.dtype[np.uint0]
UInt: TypeAlias = np.dtype[np.uint]
ULongLong: TypeAlias = np.dtype[np.ulonglong]
Inexact: TypeAlias = np.dtype[np.inexact[Any]]
Floating: TypeAlias = np.dtype[np.floating[Any]]
Float16: TypeAlias = np.dtype[np.float16]
Float32: TypeAlias = np.dtype[np.float32]
Float64: TypeAlias = np.dtype[np.float64]
Half: TypeAlias = np.dtype[np.half]
Single: TypeAlias = np.dtype[np.single]
Double: TypeAlias = np.dtype[np.double]
Float: TypeAlias = np.dtype[np.float_]
LongDouble: TypeAlias = np.dtype[np.longdouble]
LongFloat: TypeAlias = np.dtype[np.longfloat]
ComplexFloating: TypeAlias = np.dtype[np.complexfloating[Any, Any]]
Complex64: TypeAlias = np.dtype[np.complex64]
Complex128: TypeAlias = np.dtype[np.complex128]
CSingle: TypeAlias = np.dtype[np.csingle]
SingleComplex: TypeAlias = np.dtype[np.singlecomplex]
CDouble: TypeAlias = np.dtype[np.cdouble]
Complex: TypeAlias = np.dtype[np.complex_]
CFloat: TypeAlias = np.dtype[np.cfloat]
CLongDouble: TypeAlias = np.dtype[np.clongdouble]
CLongFloat: TypeAlias = np.dtype[np.clongfloat]
LongComplex: TypeAlias = np.dtype[np.longcomplex]
Flexible: TypeAlias = np.dtype[np.flexible]
Void: TypeAlias = np.dtype[np.void]
Void0: TypeAlias = np.dtype[np.void0]
Character: TypeAlias = np.dtype[np.character]
Bytes: TypeAlias = np.dtype[np.bytes_]
Str: TypeAlias = np.dtype[np.str_]
String: TypeAlias = np.dtype[np.string_]
Bytes0: TypeAlias = np.dtype[np.bytes0]
Unicode: TypeAlias = np.dtype[np.unicode_]
Str0: TypeAlias = np.dtype[np.str0]

dtype_per_name: Dict[str, np.dtype[Any]]
name_per_dtype: Dict[np.dtype[Any], str]
