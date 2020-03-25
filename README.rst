|Python versions| |PyPI version| |Downloads|

nptyping
========

Type hints for `Numpy`!

Installation
''''''''''''

::

   pip install nptyping

Usage
'''''

`nptyping.NDArray` lets you define the shape and type of your `numpy.ndarray`.

You can specify:
  * the number of dimensions;
  * the size per dimension;
  * the type of the array.


The code below illustrates how to define NDArray types:

.. code:: python

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


.. |Python versions| image:: https://img.shields.io/pypi/pyversions/nptyping.svg
   :target: https://img.shields.io/pypi/pyversions/nptyping.svg

.. |PyPI version| image:: https://badge.fury.io/py/nptyping.svg
   :target: https://badge.fury.io/py/nptyping

.. |Downloads| image:: https://img.shields.io/pypi/dm/nptyping.svg
   :target: https://pypistats.org/packages/nptyping
