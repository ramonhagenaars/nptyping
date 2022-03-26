<a href='https://https://pypi.org/project/nptyping/'>
  <img src='https://github.com/ramonhagenaars/nptyping/raw/master/resources/logo.png' />
</a> 

# *User documentation*

---


* [Introduction](#Introduction)
* [Usage](#Usage)
* [NDArray](#NDArray)
* [Shape expressions](#Shape-expressions)
    * [Syntax](#Syntax)
    * [Validation](#Validation)
    * [Normalization](#Normalization)
    * [Variables](#Variables)
    * [Wildcards](#Wildcards)
    * [N dimensions](#N-dimensions)
    * [Dimension breakdowns](#Dimension-breakdowns)
    * [Labels](#Labels)
  * [DTypes](#DTypes)
* [Examples](#Examples)
* [Similar projects](#Similar-projects)
* [FAQ](#FAQ)
* [About](#About)


## Introduction

---

Thank you for showing interest in this library.

The intended audience of this document, are Pythoneers using `numpy`, that want to make their code more readable and 
secure with type hints.

In this document, all features that `nptyping` has to offer can be found. If you think that something is missing or not
clear enough, please check the [issue section](https://github.com/ramonhagenaars/nptyping/issues) to see if you can find
your answer there. Don't forget to also check the 
[closed issues](https://github.com/ramonhagenaars/nptyping/issues?q=is%3Aissue+is%3Aclosed). Otherwise, feel free to 
raise your question [in a new issue](https://github.com/ramonhagenaars/nptyping/issues/new).

You will find a lot of code blocks in this document. If you wonder why they are written the way they are (e.g. with the 
`>>>` and the `...`): all code blocks are tested using [doctest](https://docs.python.org/3/library/doctest.html).

## Usage

---

### NDArray
The `NDArray` is the main character of this library and can be used to describe `numpy.ndarray`.

```python
>>> from nptyping import NDArray

```
The `NDArray` can take 2 arguments between brackets: the dtype and the shape of the array that is being described. This
takes the form `NDArray[Shape[<SHAPE EXPRESSION>, <DTYPE>]]`. For example:

```python
>>> from nptyping import UInt16, Shape
>>> NDArray[Shape["5, 3"], UInt16]
NDArray[Shape['5, 3'], UShort]

```
You can use `typing.Any` to denote any dtype or any shape:
```python
>>> from typing import Any
>>> NDArray[Any, Any]
NDArray[Any, Any]

```

### Shape expressions
You can denote the shape of an array using what we call a **shape expression**. This expression - a string - can be put
into `Shape` and can then be used in an `NDArray`. 
```python
>>> from nptyping import Shape

```
An example of a shape expression in an `NDArray`:
```python
>>> from typing import Any

>>> NDArray[Shape["3, 4"], Any]
NDArray[Shape['3, 4'], Any]

```
The above example shows an expression of a shape consisting of 2 dimensions of respectively size 3 and size 4. a fitting
array would be: `np.array([[11, 12, 13, 14], [21, 22, 23, 24], [31, 32, 33, 34]])`.

`Shape` is actually just an alias for `typing.Literal`:
```python
>>> Shape["2, 2"]
typing.Literal['2, 2']

```
This also means that you can use `typing.Literal` instead of `Shape` if you want.

#### Syntax

A shape expression is just a comma separated list of dimensions. A dimension can be denoted by its size, like is done in
the former examples. But you can also use variables, labels, wildcards and dimension breakdowns:
```python
>>> Shape["3, 3 withLabel, *, Var, [entry1, entry2, entry3]"]
typing.Literal['3, 3 withLabel, *, Var, [entry1, entry2, entry3]']

```
The shape expression above denotes a shape of size 3, 3, any, any, 3. For more details on the concepts of variables,
labels, wildcards and dimension breakdowns, they are described in the following sections.

The syntax of a shape expression can be formalized in BNF. Extra whitespacing is allowed (e.g. around commas), but this
is not included in the schema below (to avoid extra complexity).
```
shape-expression     =  <dimensions>|<dimension>","<ellipsis>
dimensions           =  <dimension>|<dimension>","<dimensions>
dimension            =  <unlabeled-dimension>|<labeled-dimension>
labeled-dimension    =  <unlabeled-dimension>" "<label>
unlabeled-dimension  =  <number>|<variable>|<wildcard>|<dimension-breakdown>
wildcard             =  "*"
dimension-breakdown  =  "["<labels>"]"
labels               =  <label>|<label>","<labels>
label                =  <lletter>|<lletter><word>
variable             =  <uletter>|<uletter><word>
word                 =  letter|<word><underscore>|<word><number>
letter               =  <lletter>|<uletter> 
uletter              =  "A"|"B"|"C"|"D"|"E"|"F"|"G"|"H"|"I"|"J"|"K"|"L"|"M"|"N"|"O"|"P"|"Q"|"R"|"S"|"T"|"U"|"V"|"W"|"X"|"Y"|"Z" 
lletter              =  "a"|"b"|"c"|"d"|"e"|"f"|"g"|"h"|"i"|"j"|"k"|"l"|"m"|"n"|"o"|"p"|"q"|"r"|"s"|"t"|"u"|"v"|"w"|"x"|"y"|"z"
number               =  <digit>|<number><digit> 
digit                =  "0"|"1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9"
underscore           =  "_"
ellipsis             =  "..."
```

#### Validation
Shape expressions are validated when put into an `NDArray`. Invalid expressions raise an `InvalidShapeError`.
```python
>>> from typing import Any
>>> from nptyping import NDArray, Shape, InvalidShapeError

>>> try:
...    NDArray[Shape["3, 3,"], Any]
... except InvalidShapeError as err:
...    print(err)
'3, 3,' is not a valid shape expression

```

#### Normalization
Shape expressions are normalized when put into an `NDArray`.

```python
>>> from typing import Any
>>> from nptyping import NDArray, Shape

>>> NDArray[Shape[" 3 , 3 "], Any]
NDArray[Shape['3, 3'], Any]

```

#### Variables
Variables can be used to describe dimensions of variable size:
```python
>>> from numpy import random
>>> isinstance(random.randn(2, 2), NDArray[Shape["Size, Size"], Any])
True
>>> isinstance(random.randn(100, 100), NDArray[Shape["Size, Size"], Any])
True
>>> isinstance(random.randn(42, 43), NDArray[Shape["Size, Size"], Any])
False

```
They are interpreted from left to right. This means that in the last example, upon instance checking, `Size` becomes 
`42`, which is then checked against `43`, hence the `False`.

A variable is a word that may contain underscores and digits as long as *it starts with an uppercase letter*.

#### Wildcards
A wildcard accepts any dimension size. It is denoted by the asterisk (`*`). Example:
```python
>>> isinstance(random.randn(42, 43), NDArray[Shape["*, *"], Any])
True

```

#### N dimensions
The ellipsis (`...`) can be used to denote a variable number of dimensions. For example:
```python
>>> isinstance(random.randn(2), NDArray[Shape["2, ..."], Any])
True
>>> isinstance(random.randn(2, 2, 2), NDArray[Shape["2, ..."], Any])
True
>>> isinstance(random.randn(2, 2, 3), NDArray[Shape["2, ..."], Any])
False

```
Combined with the wildcard, you could express the "any shape":

```python
>>> isinstance(random.randn(2), NDArray[Shape["*, ..."], Any])
True
>>> isinstance(random.randn(2, 42, 100), NDArray[Shape["*, ..."], Any])
True

```
The shape in the above example can be replaced with `typing.Any` to have the same effect.

#### Dimension breakdowns
A dimension can be broken down into more detail. We call this a **dimension breakdown**. This can be useful to clearly
describe what a dimension means. Example:

```python
>>> isinstance(random.randn(100, 2), NDArray[Shape["*, [x, y]"], Any])
True

```
The shape expression in the example above is synonymous to `Shape["*, 2"]`.

Dimension breakdowns must consist of one or more labels, separated by commas. In contrast to variables, labels must 
start with a lowercase letter and may contain underscores and digits.

#### Labels
Labels can be used as extra clarification in a shape expression. They can be used in dimension breakdowns and right
after dimensions. Example:
```python
>>> isinstance(random.randn(5, 2), NDArray[Shape["5 coordinates, [x, y]"], Any])
True
>>> isinstance(random.randn(5, 2), NDArray[Shape["5 coordinates, [x, y] wgs84"], Any])
True

```

### DTypes
The first argument of `NDArray` can be `typing.Any` or any of the following dtypes:
```python
>>> from nptyping.typing_ import dtypes
>>> for _, dtype_name in dtypes:
...     print(dtype_name)
Number
Bool
Bool8
Object
Object0
Datetime64
Integer
SignedInteger
Int8
Int16
Int32
Int64
Byte
Short
IntC
IntP
Int0
Int
LongLong
Timedelta64
UnsignedInteger
UInt8
UInt16
UInt32
UInt64
UByte
UShort
UIntC
UIntP
UInt0
UInt
ULongLong
Inexact
Floating
Float16
Float32
Float64
Half
Single
Double
Float
LongDouble
LongFloat
ComplexFloating
Complex64
Complex128
CSingle
SingleComplex
CDouble
Complex
CFloat
CLongDouble
CLongFloat
LongComplex
Flexible
Void
Void0
Character
Bytes
String
Bytes0
Unicode
Str0

```
These are just aliases for `numpy` dtypes.
```python
>>> from nptyping import Int
>>> Int
<class 'numpy.int32'>

```
As a result, you may also provide `numpy` dtypes directly to an `NDArray`.

## Examples

---

Here is just a list of examples of how one can express arrays with `NDArray`.

An Array with any dimensions of any size and any type:
```python
>>> from nptyping import NDArray, Shape
>>> from typing import Any


>>> NDArray[Any, Any]
NDArray[Any, Any]

>>> NDArray[Shape["*, ..."], Any]
NDArray[Any, Any]

>>> NDArray  # MyPy doesn't like this one though.
NDArray[Any, Any]

```

An array with 1 dimension of any size and any type:
```python
>>> NDArray[Shape["*"], Any]
NDArray[Shape['*'], Any]

>>> NDArray[Shape["Var"], Any]
NDArray[Shape['Var'], Any]

```

An array with 1 dimension of size 3 and any type:
```python
>>> NDArray[Shape["3"], Any]
NDArray[Shape['3'], Any]

>>> NDArray[Shape["[entry1, entry2, entry3]"], Any]
NDArray[Shape['[entry1, entry2, entry3]'], Any]

```

An array with 3 dimensions of size 3, 3 and any and any type:
```python
>>> NDArray[Shape["3, 3, *"], Any]
NDArray[Shape['3, 3, *'], Any]

>>> NDArray[Shape["3, 3, Var"], Any]
NDArray[Shape['3, 3, Var'], Any]

>>> NDArray[Shape["3, [entry1, entry2, entry3], Var"], Any]
NDArray[Shape['3, [entry1, entry2, entry3], Var'], Any]

```

A square array with 2 dimensions that are of the same size:
```python
>>> NDArray[Shape["Dim, Dim"], Any]
NDArray[Shape['Dim, Dim'], Any]

```

An array with multiple dimensions of the same size:
```python
>>> NDArray[Shape["Dim, ..."], Any]
NDArray[Shape['Dim, ...'], Any]

```

An array with 2 dimensions of any size with type unsigned int.
```python
>>> from nptyping import UInt
>>> NDArray[Shape["*, *"], UInt]
NDArray[Shape['*, *'], UInt]

```

## Similar projects

---

* [numpy.typing](https://numpy.org/devdocs/reference/typing.html) <br/>
*First and foremost, `numpy`'s own typing. The pyi files are more complete and up to date than `nptyping`'s, so if code
completion in an IDE is most important to you, this might be your go to. On the other hand, at the moment of writing, it
does not offer instance checking with shapes as `nptptying` does.*
* [dataenforce](https://github.com/CedricFR/dataenforce) <br/>
*Although not for `numpy`, this library offers type hinting for `pandas.DataFrame`. Currently, there seems to be no
`MyPy` integration, but apart from that it seems easy to use.*
* [typing.annotated](https://peps.python.org/pep-0593/) <br/>
*You could also create your own type hints using Python's builtin `typing` module. The `typing.Annotated` will take you
quite far. `MyPy` will support it (to some extent), but you won't have any instance or shape checking.*
  
## FAQ

---
* Can `MyPy` do the instance checking? <br/>
*Unfortunately no. The checking done by MyPy is limited to "`ndarray` or not an `ndarray`".*
* Will there ever be support for Pandas DataFrames? Or for Tensorflow Tensors? Or for... ? <br/>
*Maybe. Possibly. If there is enough demand for it and if I find the spare time.*

## About

---

This project started in 2019 from a personal need to keep a `numpy` project maintainable. I prototyped a very small
solution to the (then) missing type hint options for `numpy`. Then I put it online for others to use. I learned a lot
since then and I feel that I owe a lot to everyone that has contributed to this project in any way. 

I wish to thank all contributors. It amazes me everytime when someone proposes an improvement in a near-perfect pull 
request. Also, the ideas and thoughts that some people put into the discussions are very valuable to this project, I 
consider these people contributors as well.

Also thanks to all users. The best motivation for an open source fanatic like myself, is to see the software being used 
and to hear people being happy with it. This is what drives me to continue. 

Happy coding!

~ Ramon Hagenaars
