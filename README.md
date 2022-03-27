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

<br/>

<br/><br/>
<p align='center'>⚠ This describes the 2.0.0 <i>alpha</i> release.</p>
<p align='center'>For the latest stable release, pick <a href='https://pypi.org/project/nptyping/1.4.4/'>1.4.4</a></p>
<br/><br/>

💡 *Type hints for `NumPy`* <br/>
💡 *Extensive dynamic type checks for dtypes and shapes of arrays* <br/>
💡 *Limited static type checks with `MyPy`* <br/>

Example of a hinted function with `nptyping`:

```python
>>> from nptyping import NDArray, Int, Shape

>>> def func(arr: NDArray[Shape["2, 2"], Int]) -> None:
...     pass


```

Example of instance checking:
```python
>>> from numpy import array

>>> isinstance(array([[1, 2], [3, 4]]), NDArray[Shape["2, 2"], Int])
True

>>> isinstance(array([[1., 2.], [3., 4.]]), NDArray[Shape["2, 2"], Int])
False

>>> isinstance(array([1, 2, 3, 4]), NDArray[Shape["2, 2"], Int])
False

```

`nptyping` also provides `assert_isinstance`. In contrast to `assert isinstance(...)`, this won't cause IDEs or MyPy
complaints. Here is an example: 
```python
>>> from nptyping import assert_isinstance
>>> assert_isinstance(array([1]), NDArray[Shape["1"], Int])
True

```

Here is an example of how detailed expressions can become with `nptyping`:
```python
def plan_route(locations: NDArray[Shape["[from, to], [x, y]"], Float]) -> NDArray[Shape["* stops, [x, y]"], Float]:
    ...
```

More examples can be found in the [documentation](https://github.com/ramonhagenaars/nptyping/blob/master/USERDOCS.md#Examples).

## Installation

```
pip install nptyping
```

## Documentation

* [User documentation](https://github.com/ramonhagenaars/nptyping/blob/master/USERDOCS.md) <br/>
The place to go if you are using this library. <br/><br/>
  
* [Release notes](https://github.com/ramonhagenaars/nptyping/blob/master/HISTORY.md) <br/>
To see what's new, check out the release notes. <br/><br/>

* [Contributing](https://github.com/ramonhagenaars/nptyping/blob/master/CONTRIBUTION.md) <br/>
If you're interested in developing along, find the guidelines here. <br/><br/>

* [Licence](https://github.com/ramonhagenaars/nptyping/blob/master/LICENSE) <br/>
If you want to check out how open source this library is.
