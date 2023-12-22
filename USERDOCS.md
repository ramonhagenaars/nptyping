<a href='https://https://pypi.org/project/nptyping/'>
  <img src='https://github.com/ramonhagenaars/nptyping/raw/master/resources/logo.png' />
</a> 

# *User documentation*

- [*User documentation*](#user-documentation)
  - [Introduction](#introduction)
  - [Quickstart](#quickstart)
  - [Usage](#usage)
    - [NDArray](#ndarray)
    - [Shape expressions](#shape-expressions)
      - [Syntax shape expressions](#syntax-shape-expressions)
      - [Validation](#validation)
      - [Normalization](#normalization)
      - [Variables](#variables)
      - [Shape Wildcards](#shape-wildcards)
      - [N dimensions](#n-dimensions)
      - [Dimension breakdowns](#dimension-breakdowns)
      - [Labels](#labels)
    - [DTypes](#dtypes)
    - [Structure expressions](#structure-expressions)
      - [Syntax structure expressions](#syntax-structure-expressions)
      - [Subarrays](#subarrays)
      - [Structure Wildcards](#structure-wildcards)
    - [RecArray](#recarray)
    - [Pandas DataFrame](#pandas-dataframe)
    - [Examples](#examples)
  - [Similar projects](#similar-projects)
  - [FAQ](#faq)
  - [About](#about)

## Introduction

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

## Quickstart
Install `nptyping` for the type hints and the recommended `beartype` for dynamic type checks:
```shell
pip install nptyping[complete], beartype
```

Use the combination of these packages to add type safety and readability:
```python
# File: myfile.py

>>> from nptyping import DataFrame, Structure as S
>>> from beartype import beartype

>>> @beartype  # The function signature is now type safe
... def fun(df: DataFrame[S["a: Int, b: Str"]]) -> DataFrame[S["a: Int, b: Str"]]:
...     return df

```

On your production environments, run Python in optimized mode. This disables the type checks done by beartype and any
overhead it may cause:
```shell
python -OO myfile.py
```
You're now good to go. You can sleep tight knowing that today you made your codebase safer and more transparent.

## Usage

### NDArray
The `NDArray` is the main character of this library and can be used to describe `numpy.ndarray`.

```python
>>> from nptyping import NDArray

```
The `NDArray` can take 2 arguments between brackets: the dtype and the shape of the array that is being described. This
takes the form `NDArray[Shape[<SHAPE EXPRESSION>], <DTYPE>]`. For example:

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

`Shape` is actually just a rich alias for `typing.Literal`:
```python
>>> from typing import Literal

>>> Shape["2, 2"] == Literal['2, 2']
True

```
This also means that you can use `typing.Literal` instead of `Shape` if you want.

#### Syntax shape expressions

A shape expression is just a comma separated list of dimensions. A dimension can be denoted by its size, like is done in
the former examples. But you can also use variables, labels, wildcards and dimension breakdowns:
```python
>>> Shape["3, 3 withLabel, *, Var, [entry1, entry2, entry3]"]
Shape['3, 3 withLabel, *, Var, [entry1, entry2, entry3]']

```
The shape expression above denotes a shape of size 3, 3, any, any, 3. For more details on the concepts of variables,
labels, wildcards and dimension breakdowns, they are described in the following sections.

The syntax of a shape expression can be formalized in BNF. Extra whitespacing is allowed (e.g. around commas), but this
is not included in the schema below (to avoid extra complexity).
```
shape-expression     =  <dimensions>|<dimensions>","<ellipsis>
dimensions           =  <dimension>|<dimension>","<dimensions>
dimension            =  <unlabeled-dimension>|<labeled-dimension>
labeled-dimension    =  <unlabeled-dimension>" "<label>
unlabeled-dimension  =  <number>|<variable>|<wildcard>|<dimension-breakdown>
wildcard             =  "*"
dimension-breakdown  =  "["<labels>"]"
labels               =  <label>|<label>","<labels>
label                =  <lletter>|<lletter><word>
variable             =  <uletter>|<uletter><word>
word                 =  <letter>|<word><underscore>|<word><number>
letter               =  <lletter>|<uletter> 
uletter              =  "A"|"B"|"C"|"D"|"E"|"F"|"G"|"H"|"I"|"J"|"K"|"L"|"M"|"N"|"O"|"P"|"Q"|"R"|"S"|"T"|"U"|"V"|"W"|"X"|"Y"|"Z" 
lletter              =  "a"|"b"|"c"|"d"|"e"|"f"|"g"|"h"|"i"|"j"|"k"|"l"|"m"|"n"|"o"|"p"|"q"|"r"|"s"|"t"|"u"|"v"|"w"|"x"|"y"|"z"
number               =  <digit>|<number><digit> 
digit                =  "0"|"1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9"
underscore           =  "_"
ellipsis             =  "..."
```

#### Validation
Shape expressions are validated and may raise an `InvalidShapeError`.
```python
>>> from nptyping import Shape, InvalidShapeError

>>> try:
...    Shape["3, 3,"]
... except InvalidShapeError as err:
...    print(err)
'3, 3,' is not a valid shape expression.

```

#### Normalization
Shape expressions are normalized, so your "shape expression style" won't affect its working.

```python
>>> from nptyping import Shape

>>> Shape[" 3 , 3 "]
Shape['3, 3']

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

#### Shape Wildcards
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

You can also express "at least N dimensions":
```python
>>> isinstance(random.randn(2, 2), NDArray[Shape["2, 2, ..."], Any])
True
>>> isinstance(random.randn(2, 2, 2, 2), NDArray[Shape["2, 2, ..."], Any])
True
>>> isinstance(random.randn(2), NDArray[Shape["2, 2, ..."], Any])
False

```

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
The second argument of `NDArray` can be `typing.Any` or any of the following dtypes:
```python
>>> from nptyping.typing_ import dtypes
>>> for _, dtype_name in dtypes:
...     print(dtype_name)
Number
Bool
Obj
Object
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
Character
Bytes
String
Str
Unicode

```
These are special aliases for `numpy` dtypes.
```python
>>> from nptyping import Int
>>> Int
<class 'numpy.integer'>

```
You may also provide `numpy` dtypes directly to an `NDArray`. This is <strong>not</strong> recommended though, because 
MyPy won't accept it.
```python
>>> import numpy as np

>>> NDArray[Any, np.floating]
NDArray[Any, Floating]

```

### Structure expressions
You can denote the structure of a structured array using what we call a **structure expression**. This expression 
(again a string) can be put into `Structure` and can then be used in an `NDArray`.
```python
>>> from nptyping import Structure

```
An example of a structure expression in an `NDArray`:
```python
>>> from typing import Any

>>> NDArray[Any, Structure["name: Str, age: Int"]]
NDArray[Any, Structure['age: Int, name: Str']]

```
The above example shows an expression for a structured array with 2 fields.

Like with `Shape`, you can use `typing.Literal` in an `NDArray`:
```python
>>> from typing import Literal

>>> Structure["x: Float, y: Float"] == Literal["x: Float, y: Float"]
True

```
This also means that you can use `typing.Literal` instead of `Structure` if you want.

#### Syntax structure expressions

A structure expression is a comma separated list of fields, with each field consisting of a name and a type.
```python
>>> Structure["a_name: AType, some_other_name: SomeOtherType"]
Structure['a_name: AType, some_other_name: SomeOtherType']

```

You can combine fields if you want to express multiple names with the same type. Here is an example of how that may
look:
```python
>>> from nptyping import Structure

>>> Structure["[a, b, c]: Int, [d, e, f]: Float"]
Structure['[d, e, f]: Float, [a, b, c]: Int']

```

It can make your expression more concise, but it's just an alternative way of expressing the same thing:
```python
>>> from nptyping import Structure

>>> Structure["a: Int, b: Int, c: Int, d: Float, e: Float, f: Float"] \
... is \
... Structure["[a, b, c]: Int, [d, e, f]: Float"]
True

```

The syntax of a structure expression can be formalized in BNF. Extra whitespacing is allowed (e.g. around commas and 
colons), but this is not included in the schema below.
```
structure-expression  =  <fields>|<fields>","<wildcard>
fields                =  <field>|<field>","<fields>
field                 =  <field-name>":"<field-type>|"["<combined-field-names>"]:"<field-type>
combined-field-names  =  <field-name>","<field-name>|<field-name>","<combined-field-names>
field-type            =  <word>|<word><field-subarray-shape>|<wildcard>
wildcard              =  "*"
field-subarray-shape  = "["<shape-expression>"]"
field-name            =  <word>
word                  =  <letter>|<word><underscore>|<word><number>
letter                =  <lletter>|<uletter> 
uletter               =  "A"|"B"|"C"|"D"|"E"|"F"|"G"|"H"|"I"|"J"|"K"|"L"|"M"|"N"|"O"|"P"|"Q"|"R"|"S"|"T"|"U"|"V"|"W"|"X"|"Y"|"Z" 
lletter               =  "a"|"b"|"c"|"d"|"e"|"f"|"g"|"h"|"i"|"j"|"k"|"l"|"m"|"n"|"o"|"p"|"q"|"r"|"s"|"t"|"u"|"v"|"w"|"x"|"y"|"z"
number                =  <digit>|<number><digit> 
digit                 =  "0"|"1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9"
underscore            =  "_"
```

#### Subarrays
You can express the shape of a subarray using brackets after a type. You can use the full power of shape expressions.

```python
>>> from typing import Any
>>> import numpy as np
>>> from nptyping import NDArray, Structure

>>> arr = np.array([("x")], np.dtype([("x", "U10", (2, 2))]))
>>> isinstance(arr, NDArray[Any, Structure["x: Str[2, 2]"]])
True

```

#### Structure Wildcards
You can use wildcards for field types or globally (for complete fields).
Here is an example of a wildcard for a field type:
```python
>>> Structure["anyType: *"]
Structure['anyType: *']

```

And here is an example with a global wildcard:
```python
>>> Structure["someType: int, *"]
Structure['someType: int, *']

```
This expresses a structure that has *at least* a field `someType: int`. Any other fields are also accepted.

### RecArray
The `RecArray` corresponds to [numpy.recarray](https://numpy.org/doc/stable/reference/generated/numpy.recarray.html).
It is an extension of `NDArray` and behaves similarly. A key difference is that with `RecArray`, the `Structure` OR 
`typing.Any` are mandatory. 

```python
>>> from nptyping import RecArray

>>> RecArray[Any, Structure["x: Float, y: Float"]]
RecArray[Any, Structure['[x, y]: Float']]

```

### Pandas DataFrame
The `nptyping.DataFrame` can be used for expressing structures of `pandas.DataFrame`. It takes a `Structure` and uses
the same Structure Expression syntax. 

```python
>>> from nptyping import DataFrame, Structure as S

>>> DataFrame[S["name: Str, x: Float, y: Float"]]
DataFrame[Structure['[x, y]: Float, name: Str']]

```

Check out the documentation on [Structure Expressions](#Structure-expressions) for more details.

### Examples

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

An array with 2 dimensions of size 3 and 3 with a structured type.
```python
>>> NDArray[Shape["3, 3"], Structure["x: Float, y: Float"]]
NDArray[Shape['3, 3'], Structure['[x, y]: Float']]

```

Here are some examples of rich expressions that `nptyping` facilitates:
```python
>>> from nptyping import NDArray, Shape, Float

>>> def plan_route(
...        locations: NDArray[Shape["[from, to], [x, y]"], Float]
... ) -> NDArray[Shape["* stops, [x, y]"], Float]:
...   ...

>>> AssetArray = NDArray[Shape["* assets, [id, type, age, state, x, y]"], Float]

>>> def get_assets_within_range(
...     x: float, y: float, range_km: float, assets: AssetArray
... ) -> AssetArray:
...     ...

```

Here is an example of how to get type safety to the max, by stacking `nptyping` up with
[beartype](https://github.com/beartype/beartype):
```python
>>> from beartype import beartype

>>> @beartype
... def type_safety(assets: AssetArray) -> None:
...     # assets is now guaranteed by beartype to be an AssetArray.
...     ...

```

## Similar projects

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

* PyCharm complains about `Shape[<expression>]`, what should I do? <br/>
*Unfortunately, some IDEs try to parse what's between quotes in a type hint sometimes. You are left with 3 options:*
  1. *Use `typing.Literal` instead of `Shape`, `nptyping` can handle this perfectly fine*
  2. *Use an extra pair of quotes: `Shape['"<expression>"']`*, this appeases PyCharm and is accepted by `nptyping`
  3. *Do nothing, accept the IDE complaints, wait and hope for the IDE to mature*
* Can `MyPy` do the instance checking? <br/>
*Because of the dynamic nature of `numpy` and `pandas`, this is currently not possible. The checking done by MyPy is* 
*limited to detecting whether or not a `numpy` or `pandas` type is provided when that is hinted. There are no static*
*checks on shapes, structures or types.*
* Will there ever be support for Tensorflow Tensors? Or for... ? <br/>
*Maybe. Possibly. If there is enough demand for it and if I find the spare time.*

## About

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
