[![PyPI version](https://img.shields.io/pypi/pyversions/nptyping.svg)](https://img.shields.io/pypi/pyversions/nptyping.svg)
[![Downloads](https://pepy.tech/badge/nptyping/month)](https://pepy.tech/project/nptyping/month)
[![PyPI version](https://badge.fury.io/py/nptyping.svg)](https://badge.fury.io/py/nptyping)
[![codecov](https://codecov.io/gh/ramonhagenaars/nptyping/branch/master/graph/badge.svg)](https://codecov.io/gh/ramonhagenaars/nptyping)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/ramonhagenaars/nptyping/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/ramonhagenaars/nptyping/?branch=master)

# nptyping

Type hints for `Numpy`!

## Installation

```
pip install nptyping
```

## Usage

### NDArray

`nptyping.NDArray` lets you define the shape and type of your `numpy.ndarray`.

You can:
  * specify the number of dimensions;
  * specify the size per dimension;
  * specify the type of the array;
  * instance check your array with your nptying type.

#### Examples

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
>>> NDArray[int]
NDArray[(typing.Any, ...), int]

>>> NDArray[(Any, ...), int]
NDArray[(typing.Any, ...), int]

```

An array with 1 dimension of size 3 and type int:
```python
>>> NDArray[3, int]
NDArray[(3,), int]

>>> NDArray[(3,), int]
NDArray[(3,), int]

```

An array with any dimensions of size 3 and type int:
```python
>>> NDArray[(3, ...), int]
NDArray[(3, ...), int]

```

An array with 3 dimensions of sizes 3, 3, 5 and type int:
```python
>>> NDArray[(3, 3, 5), int]
NDArray[(3, 3, 5), int]

```

#### Checking your instances
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

#### Finding the right annotation
You can use `NDArray` to find the type of a numpy array for you using `NDArray.type_of`:

```python
>>> NDArray.type_of(np.array([[1, 2], [3, 4.0]]))
NDArray[(2, 2), float64]

```

### py_type
With `py_type` you can get the Python builtin type that corresponds to a Numpy `dtype`:

```python
>>> from nptyping import py_type

>>> py_type(np.int32)
<class 'int'>

```
