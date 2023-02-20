# History

## 2.5.0 (2023-02-06)

- Added the column wildcard in structure expressions to allow expressing 'a structure with at least ...'. 
- Fixed the `help` text for functions that use `nptyping` types as hints.
- Fixed the distribution of `dataframe.pyi` that was missing.
- Fixed the sdist to include tests and dependencies.

## 2.4.1 (2022-11-16)

- Fixed compatibility with `mypy==0.991`.

## 2.4.0 (2022-11-14)

- Added hint for pandas DataFrame.
- Fixed bug for checking against a Structure where a different number of fields did not fail the check. 
- Changed `nptyping.Int` pointing to the more generic `numpy.integer` rather than `numpy.int32`.
- Added support for Python 3.11 with the exception of `pandas.DataFrame`.

## 2.3.1 (2022-08-30)

- Fixed mypy error of inheriting final dtype as of numpy==1.23.1.
- Allowed for quotes in shape expressions to appease PyCharm.

## 2.3.0 (2022-08-28)

- Added support for subarrays with shape expressions inside structure expressions.
- Added support for wildcards in structure expressions.

## 2.2.0 (2022-06-26)

- Added support for expressing "at least N dimensions".

## 2.1.3 (2022-06-19)

- Fixed typing issue with Pyright/Pylance that caused the message: "Literal" is not a class
- Fixed wrong error message when an invalid `Structure` was provided to `NDArray`.

## 2.1.2 (2022-06-08)

- Fixed bug that caused MyPy to fail with the message: Value of type variable "_DType_co" of "ndarray" cannot be "floating[Any]"

## 2.1.1 (2022-06-01)

- Fixed bug that numpy ndarrays were incorrectly instance checked against `RecArray`.

## 2.1.0 (2022-06-01)

- Added `Structure` and "structure expressions" to support structured arrays.
- Added `RecArray`.

## 2.0.1 (2022-04-28)

Thanks to [Jasha10](https://github.com/Jasha10) for this release.
- Added an improved default message for `assert_isinstance`.
  
Also some typos in README, in `test_mypy.py` and some style corrections.

## 2.0.0 (2022-04-07)

Changes since `1.4.4`:
- Changed the interface of `NDArray` into `NDArray[SHAPE, DTYPE]`
- Added MyPy-acceptance (limited static type checking)
- Added support for variables
- Added support for labels and named dimensions
- Added support for all numpy dtypes with `NDArray`
- Added support for dynamic type checker: beartype
- Added support for dynamic type checker: typeguard
- Added autocompletion for all attributes of `ndarray`
- Added CONTRIBUTING.md
- Removed support for Python 3.5 and Python 3.6

## 2.0.0a2 (2022-03-27)

- Changed the interface of `NDArray`: switched the order to `NDArray[SHAPE, DTYPE]` to be compatible to `numpy.ndarray.pyi`
- Added autocompletion for all attributes of `ndarray` by changing the implementation of `NDArray`
- Added CONTRIBUTING.md
- Added support for dynamic type checker: beartype
- Added support for dynamic type checker: typeguard

## 2.0.0a1 (2022-03-19)

- Changed the interface of `NDArray`
- Added MyPy-acceptance (limited static type checking)
- Added support for variables
- Added support for labels and named dimensions
- Added support for all numpy dtypes with `NDArray`
- Removed support for Python 3.5 and Python 3.6

## 1.4.4 (2021-09-10)

- Fixed instance checks with 0d arrays.

## 1.4.3 (2021-08-05)

- Fixed setup.py to exclude test(-resources) in the wheel.

## 1.4.2 (2021-05-08)

- Fixed instance check that was incompatible with `typish==1.9.2`.

## 1.4.1 (2021-03-23)

- Fixed instance checks of some types that did not properly respond to non-numpy types.
- Fixed instance checks with ``nptyping.Object``.
- Fixed identities of NPTyping instances: ``NDArray[(3,), int] is NDArray[(3,), int]``.

## 1.4.0 (2020-12-23)

- Added ``SubArrayType``
- Added ``StructuredType``
- Added support for unsigned integers with ``py_type``.

## 1.3.0 (2020-07-21)

- Added ``Complex128``

## 1.2.0 (2020-06-20)

- Added ``Bool``
- Added ``Datetime64``
- Added ``Timedelta64``

## 1.1.0 (2020-05-30)

- Removed ``Array``
- Added ``get_type``
- Added ``Int``
- Added ``UInt``
- Added ``Float``
- Added ``Unicode``
- Added ``Number``
- Added ``NPType``

## 1.0.1 (2020-04-05)

- Added a hash function to ``_NDArrayMeta``.

## 1.0.0 (2020-03-22)

- Added ``NDArray``
- Deprecated ``Array``

## 0.3.0 (2019-09-11)

- Forbidden instantiation of ``Array``
- Added support for hinting ndarray methods

## 0.2.0 (2019-02-09)

- Added support for heterogeneous arrays
- Added HISTORY.rst

## 0.1.0 (2019-02-05)

- Initial release
