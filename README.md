[![PyPI version](https://img.shields.io/pypi/pyversions/nptyping.svg)](https://img.shields.io/pypi/pyversions/nptyping.svg)
[![Downloads](https://pepy.tech/badge/nptyping/month)](https://pepy.tech/project/nptyping)
[![PyPI version](https://badge.fury.io/py/nptyping.svg)](https://badge.fury.io/py/nptyping)
[![codecov](https://codecov.io/gh/ramonhagenaars/nptyping/branch/master/graph/badge.svg)](https://codecov.io/gh/ramonhagenaars/nptyping)
[![Code style](https://img.shields.io/badge/code%20style-black-black)](https://img.shields.io/badge/code%20style-black-black)


<p align='center'>
  <a href='https://https://pypi.org/project/nptyping/'>
    <img src='https://github.com/ramonhagenaars/nptyping/raw/master/resources/logo.png' />
  </a> 
</p>

💡 *Type hints for `NumPy`* <br/>
💡 *Extends `numpy.typing`* <br/>
💡 *Extensive dynamic type checks for dtypes and shapes of arrays* <br/>

Example of a hinted function with `nptyping`:

```python
>>> from nptyping import NDArray, Int, Shape

>>> def func(arr: NDArray[Shape["2, 2"], Int]) -> None:
...     pass

```

### Installation
```
pip install nptyping
```

### Instance checking

Example of instance checking:
```python
>>> import numpy as np

>>> isinstance(np.array([[1, 2], [3, 4]]), NDArray[Shape["2, 2"], Int])
True

>>> isinstance(np.array([[1., 2.], [3., 4.]]), NDArray[Shape["2, 2"], Int])
False

>>> isinstance(np.array([1, 2, 3, 4]), NDArray[Shape["2, 2"], Int])
False

```

`nptyping` also provides `assert_isinstance`. In contrast to `assert isinstance(...)`, this won't cause IDEs or MyPy
complaints. Here is an example: 
```python
>>> from nptyping import assert_isinstance

>>> assert_isinstance(np.array([1]), NDArray[Shape["1"], Int])
True

```

### Structured arrays

You can also express structured arrays using `nptyping.Structure`:
```python
>>> from nptyping import Structure

>>> Structure["name: Str, age: Int"]
Structure['age: Int, name: Str']

```

Here is an example to see it in action:
```python
>>> from typing import Any
>>> import numpy as np
>>> from nptyping import NDArray, Structure

>>> arr = np.array([("Peter", 34)], dtype=[("name", "U10"), ("age", "i4")])
>>> isinstance(arr, NDArray[Any, Structure["name: Str, age: Int"]])
True

```

### More examples

Here is an example of a rich expression that can be done with `nptyping`:
```python
def plan_route(
        locations: NDArray[Shape["[from, to], [x, y]"], Float]
) -> NDArray[Shape["* stops, [x, y]"], Float]:
    ...
```

More examples can be found in the [documentation](https://github.com/ramonhagenaars/nptyping/blob/master/USERDOCS.md#Examples).

## Documentation

* [User documentation](https://github.com/ramonhagenaars/nptyping/blob/master/USERDOCS.md) <br/>
The place to go if you are using this library. <br/><br/>
  
* [Release notes](https://github.com/ramonhagenaars/nptyping/blob/master/HISTORY.md) <br/>
To see what's new, check out the release notes. <br/><br/>

* [Contributing](https://github.com/ramonhagenaars/nptyping/blob/master/CONTRIBUTING.md) <br/>
If you're interested in developing along, find the guidelines here. <br/><br/>

* [Licence](https://github.com/ramonhagenaars/nptyping/blob/master/LICENSE) <br/>
If you want to check out how open source this library is.
