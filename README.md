[![PyPI version](https://img.shields.io/pypi/pyversions/nptyping.svg)](https://img.shields.io/pypi/pyversions/nptyping.svg)
[![Downloads](https://pepy.tech/badge/nptyping/month)](https://pepy.tech/project/nptyping)
[![PyPI version](https://badge.fury.io/py/nptyping.svg)](https://badge.fury.io/py/nptyping)
[![codecov](https://codecov.io/gh/ramonhagenaars/nptyping/branch/master/graph/badge.svg)](https://codecov.io/gh/ramonhagenaars/nptyping)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/ramonhagenaars/nptyping/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/ramonhagenaars/nptyping/?branch=master)

<p align='center'>
  <a href='https://https://pypi.org/project/nptyping/'>
    <img src='https://github.com/ramonhagenaars/nptyping/raw/master/resources/logo.png' />
  </a> 
</p>

<br/>

💡 *Type hints for `NumPy`* <br/>
💡 *Extensive dynamic type checks for dtypes and shapes of arrays* <br/>
💡 *Limited static type checks with `MyPy`* <br/>

Example of a hinted function with `nptyping`:

```python
>>> from nptyping import NDArray, Int, Shape

>>> def func(arr: NDArray[Int, Shape["2, 2"]]) -> None:
...     pass


```

Example of instance checking:
```python
>>> from numpy import array

>>> isinstance(array([[1, 2], [3, 4]]), NDArray[Int, Shape["2, 2"]])
True

>>> isinstance(array([[1., 2.], [3., 4.]]), NDArray[Int, Shape["2, 2"]])
False

>>> isinstance(array([1, 2, 3, 4]), NDArray[Int, Shape["2, 2"]])
False

```

Here is an example of how detailed expressions can become with `nptyping`:
```python
def plan_route(locations: NDArray[Float, Shape["[from, to], [x, y]"]]) -> NDArray[Float, Shape["* stops, [x, y]"]]:
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
