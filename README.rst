|PyPI version| |Build Status|

nptyping
========

Type hints for `Numpy`!

Installation
''''''''''''

::

   pip install nptyping

Usage
'''''

Use the `nptyping` type hints like the regular type hints from `typing`:

.. code:: python

   from nptyping import Array


   def func1(arr: Array[int]):
       # A numpy.ndarray that contains numbers
       ...

You can also define the shape of an array:

.. code:: python

   Array[str, 3, 2]    # 3 rows and 2 columns
   Array[str, 3]       # 3 rows and an undefined number of columns
   Array[str, 3, ...]  # 3 rows and an undefined number of columns
   Array[str, ..., 2]  # an undefined number of rows and 2 columns

`nptyping` also supports instance checks:

.. code:: python

   import numpy


   arr = numpy.array([[1, 2],
                      [3, 4],
                      [5, 6]])

   isinstance(arr, Array[int, 3, 2])    # True
   isinstance(arr, Array[str, 3, 2])    # False
   isinstance(arr, Array[int, 3, ...])  # True
   isinstance(arr, Array[int, 3, 6])    # False

.. |PyPI version| image:: https://badge.fury.io/py/nptyping.svg
   :target: https://badge.fury.io/py/nptyping

.. |Build Status| image:: https://api.travis-ci.org/ramonhagenaars/nptyping.svg?branch=master
   :target: https://travis-ci.org/ramonhagenaars/nptyping
