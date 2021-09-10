[![PyPI version](https://img.shields.io/pypi/pyversions/nptyping.svg)](https://img.shields.io/pypi/pyversions/nptyping.svg)
[![Downloads](https://pepy.tech/badge/nptyping/month)](https://pepy.tech/project/nptyping)
[![PyPI version](https://badge.fury.io/py/nptyping.svg)](https://badge.fury.io/py/nptyping)
[![codecov](https://codecov.io/gh/ramonhagenaars/nptyping/branch/master/graph/badge.svg)](https://codecov.io/gh/ramonhagenaars/nptyping)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/ramonhagenaars/nptyping/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/ramonhagenaars/nptyping/?branch=master)

Type hints with dynamic checks for `Numpy`!

<p align='center'>
  <a href='https://https://pypi.org/project/nptyping/'>
    <img src='https://github.com/ramonhagenaars/nptyping/raw/master/resources/logo.png' />
  </a> 
</p>



## (❒) Installation

```
pip install nptyping
```

## (❒) Usage

### (❒) NDArray

`nptyping.NDArray` lets you define the shape and type of your `numpy.ndarray`.

You can:
  * specify the number of dimensions;
  * specify the size per dimension;
  * specify the type of the array;
  * instance check your array with your nptying type.

#### (❒) Examples

An Array with any dimensions of any size and any type:
```python
>>> from nptyping import NDArray
>>> from typing import Any


>>> NDArray
NDArray[(typing.Any, ...), typing.Any]

>>> NDArray[(Any, ...)]
NDArray[(typing.Any, ...), typing.Any]

>>> NDArray[(Any, ...), Any]
NDArray[(typing.Any, ...), typing.Any]

```

An array with 1 dimension of any size and any type:
```python
>>> NDArray[Any]
NDArray[(typing.Any,), typing.Any]

>>> NDArray[(Any,)]
NDArray[(typing.Any,), typing.Any]

>>> NDArray[Any, Any]
NDArray[(typing.Any,), typing.Any]

>>> NDArray[(Any,), Any]
NDArray[(typing.Any,), typing.Any]

```

An array with 1 dimension of size 3 and any type:
```python
>>> NDArray[3]
NDArray[(3,), typing.Any]

>>> NDArray[(3,)]
NDArray[(3,), typing.Any]

>>> NDArray[(3,), Any]
NDArray[(3,), typing.Any]

```

An array with 3 dimensions of size 3, 3 and any and any type:
```python
>>> NDArray[3, 3, Any]
NDArray[(3, 3, typing.Any), typing.Any]

>>> NDArray[(3, 3, Any)]
NDArray[(3, 3, typing.Any), typing.Any]

>>> NDArray[(3, 3, Any), Any]
NDArray[(3, 3, typing.Any), typing.Any]

```

An array with any dimensions of any size and type int:
```python
>>> import numpy as np

>>> NDArray[np.int32]
NDArray[(typing.Any, ...), Int[32]]

>>> NDArray[(Any, ...), np.int32]
NDArray[(typing.Any, ...), Int[32]]

```
Note that provided types are translated to nptyping types. 
Pure Python types (.e.g `int` or `float` are supported as well).
You can also provide nptyping types yourself: `NDArray[(Any, ...), Int[64]]`.

An array with 1 dimension of size 3 and type int:
```python
>>> NDArray[3, np.int32]
NDArray[(3,), Int[32]]

>>> NDArray[(3,), np.int32]
NDArray[(3,), Int[32]]

```

An array with any dimensions of size 3 and type int:
```python
>>> NDArray[(3, ...), np.int32]
NDArray[(3, ...), Int[32]]

```

An array with 3 dimensions of sizes 3, 3, 5 and type int:
```python
>>> NDArray[(3, 3, 5), np.int32]
NDArray[(3, 3, 5), Int[32]]

```

A structured array:
```python
>>> import numpy as np

>>> NDArray[(Any,...), np.dtype([('x',np.int32), ('y',np.int32)])]
NDArray[(typing.Any, ...), StructuredType[Int[32], Int[32]]]

```

#### (❒) Checking your instances
You can use `NDArray` with `isinstance` to dynamically check your arrays.

```python
>>> import numpy as np

>>> arr = np.array([[1, 2, 3],
...                 [4, 5, 6]])

>>> isinstance(arr, NDArray[(2, 3), int])
True
>>> isinstance(arr, NDArray[(2, 3), float])
False
>>> isinstance(arr, NDArray[(2, 3, 1), int])
False

```

#### (❒) Finding the right annotation
You can use `NDArray` to find the type of a numpy array for you using `NDArray.type_of`:

```python
>>> NDArray.type_of(np.array([[1, 2], [3, 4.0]]))
NDArray[(2, 2), Float[64]]

```

See also `nptyping.get_type` (documented below).

### (❒) Int
An nptyping equivalent of numpy signed integers.

```python
>>> from nptyping import Int

>>> Int[32]
Int[32]

```
You can also use one of these:
```python
>>> from nptyping import Int8, Int16, Int32, Int64

```

### (❒) UInt
An nptyping equivalent of numpy unsigned integers.

```python
>>> from nptyping import UInt

>>> UInt[64]
UInt[64]

```
You can also use one of these:
```python
>>> from nptyping import UInt8, UInt16, UInt32, UInt64

```

### (❒) Float
An nptyping equivalent of numpy floats.

```python
>>> from nptyping import Float

>>> Float[64]
Float[64]

```
You can also use one of these:
```python
>>> from nptyping import Float16, Float32, Float64

```

### (❒) Unicode
An nptyping equivalent of numpy unicodes.

```python
>>> from nptyping import Unicode

>>> Unicode[100]
Unicode[100]

```

### (❒) Bool
An nptyping equivalent of numpy bool.

```python
>>> from nptyping import Bool

>>> Bool
Bool

```

### (❒) Complex128
An nptyping equivalent of numpy complex128.

```python
>>> from nptyping import Complex128

>>> Complex128
Complex128

```

### (❒) Datetime64
An nptyping equivalent of numpy datetime64.

```python
>>> from nptyping import Datetime64

>>> Datetime64
Datetime64

```

### (❒) Timedelta64
An nptyping equivalent of numpy timedelta64.

```python
>>> from nptyping import Timedelta64

>>> Timedelta64
Timedelta64

```

### (❒) Object
An nptyping equivalent of numpy objects.

```python
>>> from nptyping import Object

>>> Object
Object

```

### (❒) StructuredType
An nptyping equivalent of numpy structured dtypes.

```python
>>> from nptyping import StructuredType, Int

>>> StructuredType[Int[32], Int[32]]
StructuredType[Int[32], Int[32]]

```

### (❒) SubArrayType
An nptyping equivalent of numpy subarray dtypes.

```python
>>> from nptyping import SubArrayType, Int

>>> SubArrayType[Int[16], (4,2)]
SubArrayType[Int[16], (4, 2)]

```

### (❒) get_type
With `get_type` you can get `nptyping` equivalent types for your arguments:

```python
>>> from nptyping import get_type

>>> get_type(np.int32)
Int[32]
>>> get_type('some string')
Unicode[11]
>>> get_type(np.dtype([('x', np.int32), ('y', np.int32)]))
StructuredType[Int[32], Int[32]]

```

### (❒) py_type
With `py_type` you can get the Python builtin type that corresponds to a Numpy `dtype`:

```python
>>> from nptyping import py_type

>>> py_type(np.int32)
<class 'int'>

```
