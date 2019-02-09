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


   def func1(arr: Array[int]):  # A numpy.ndarray that contains numbers
       ...

You can also define the shape of an array:

.. code:: python

   Array[str, 3, 2]    # 3 rows and 2 columns
   Array[str, 3]       # 3 rows and an undefined number of columns
   Array[str, 3, ...]  # 3 rows and an undefined number of columns
   Array[str, ..., 2]  # an undefined number of rows and 2 columns

Heterogeneous arrays are supported as well:

.. code:: python

   Array[int, float, str]       # int, float and str on columns 1, 2 and 3 resp.
   Array[int, float, str, ...]  # int, float and str on columns 1, 2 and 3 resp.
   Array[int, float, str, 3]    # 3 rows and int, float and str on columns 1, 2 and 3 resp.

`nptyping` also supports instance checks:

.. code:: python

   import numpy
   from nptyping import Array


   arr = numpy.array([[1, 2],
                      [3, 4],
                      [5, 6]])

   isinstance(arr, Array[int, 3, 2])    # True
   isinstance(arr, Array[str, 3, 2])    # False
   isinstance(arr, Array[int, 3, ...])  # True
   isinstance(arr, Array[int, 3, 6])    # False

Also for heterogeneous arrays:

.. code:: python

      import numpy
      from nptyping import Array


      arr = np.array([(1, 2.0, '3'),
                      (4, 5.0, '6')],
                     dtype=[('a', int), ('b', float), ('c', str)])

      isinstance(arr, Array[int, float, str])     # True
      isinstance(arr, Array[float, float, str])   # False
      isinstance(arr, Array[int, float, str, 2])  # True


.. include:: HISTORY.rst


.. |PyPI version| image:: https://badge.fury.io/py/nptyping.svg
   :target: https://badge.fury.io/py/nptyping

.. |Build Status| image:: https://api.travis-ci.org/ramonhagenaars/nptyping.svg?branch=master
   :target: https://travis-ci.org/ramonhagenaars/nptyping