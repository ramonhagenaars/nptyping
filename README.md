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

You can specify:
  * the number of dimensions;
  * the size per dimension;
  * the type of the array.

The code below illustrates how to define NDArray types:

```python
from nptyping import NDArray


# An Array with any dimensions of any size and any type.
NDArray
NDArray[(Any, ...)]
NDArray[(Any, ...), Any]

# An array with 1 dimension of any size and any type.
NDArray[Any]
NDArray[(Any,)]
NDArray[Any, Any]
NDArray[(Any,), Any]

# An array with 1 dimension of size 3 and any type.
NDArray[3]
NDArray[(3,)]
NDArray[(3,), Any]

# An array with 3 dimensions of size 3, 3 and any and any type.
NDArray[3, 3, Any]
NDArray[(3, 3, Any)]
NDArray[(3, 3, Any), Any]

# An array with any dimensions of any size and type int.
NDArray[int]
NDArray[(Any, ...), int]

# An array with 1 dimension of size 3 and type int.
NDArray[3, int]
NDArray[(3,), int]

# An array with any dimensions of size 3 and type int.
NDArray[(3, ...), int]

# An array with 3 dimensions of sizes 3, 3, 5 and type int.
NDArray[(3, 3, 5), int]
```

You can use `NDArray` to find the type of a numpy array for you using `NDArray.type_of`:

```python
>>> import numpy as np
>>> from nptyping import NDArray
>>> NDArray.type_of(np.array([[1, 2], [3, 4.0]]))
NDArray[(2, 2), float]
```

### py_type
With `py_type` you can get the Python builtin type that corresponds to a Numpy `dtype`:

```python
>>> import numpy as np
>>> from nptyping import py_type
>>> py_type(np.int32)
<class 'int'>
```
