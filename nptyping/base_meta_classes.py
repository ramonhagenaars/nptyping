"""
MIT License

Copyright (c) 2023 Ramon Hagenaars

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from abc import ABCMeta, abstractmethod
from inspect import FrameInfo
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    TypeVar,
)

from nptyping.error import InvalidArgumentsError, NPTypingError

_T = TypeVar("_T")


class InconstructableMeta(ABCMeta):
    """
    Makes it impossible for a class to get instantiated.
    """

    def __call__(cls, *_: Any, **__: Any) -> None:
        raise NPTypingError(
            f"Cannot instantiate nptyping.{cls.__name__}. Did you mean to use [ ] ?"
        )


class ImmutableMeta(ABCMeta):
    """
    Makes it impossible to changes values on a class.
    """

    def __setattr__(cls, key: str, value: Any) -> None:
        if key not in ("_abc_impl", "__abstractmethods__"):
            raise NPTypingError(f"Cannot set values to nptyping.{cls.__name__}.")


class FinalMeta(ABCMeta):
    """
    Makes it impossible for classes to inherit from some class.

    An concrete inheriting meta class requires to define a name for its
    implementation. The class with this name will be the only class that is
    allowed to use that concrete meta class.
    """

    _name_per_meta_cls: Dict[type, Optional[str]] = {}

    def __init_subclass__(cls, implementation: Optional[str] = None) -> None:
        # implementation is made Optional here, to allow other meta classes to
        # inherit.
        cls._name_per_meta_cls[cls] = implementation

    def __new__(cls, name: str, *args: Any, **kwargs: Any) -> type:
        if name == cls._name_per_meta_cls[cls]:
            assert name, "cls_name not set"
            return type.__new__(cls, name, *args, **kwargs)

        raise NPTypingError(f"Cannot subclass nptyping.{cls._name_per_meta_cls[cls]}.")


class MaybeCheckableMeta(ABCMeta):
    """
    Makes instance and subclass checks raise by default.
    """

    def __instancecheck__(cls, instance: Any) -> bool:
        raise NPTypingError(
            f"Instance checking is not supported for nptyping.{cls.__name__}."
        )

    def __subclasscheck__(cls, subclass: Any) -> bool:
        raise NPTypingError(
            f"Subclass checking is not supported for nptyping.{cls.__name__}."
        )


class PrintableMeta(ABCMeta):
    """
    Ensures that a class can be printed nicely.
    """

    @abstractmethod
    def __str__(cls) -> str:
        ...  # pragma: no cover

    def __repr__(cls) -> str:
        return str(cls)


class SubscriptableMeta(ABCMeta):
    """
    Makes a class subscriptable: it accepts arguments between brackets and a
    new type is returned for every unique set of arguments.
    """

    _all_types: Dict[Tuple[type, Tuple[Any, ...]], type] = {}
    _parameterized: bool = False

    @abstractmethod
    def _get_item(cls, item: Any) -> Tuple[Any, ...]:
        ...  # pragma: no cover

    def _get_module(cls, stack: List[FrameInfo], module: str) -> str:
        # The magic below makes Python's help function display a meaningful
        # text with nptyping types.
        return "typing" if stack[1][3] == "formatannotation" else module

    def _get_additional_values(
        cls, item: Any  # pylint: disable=unused-argument
    ) -> Dict[str, Any]:
        # This method is invoked after _get_item and right before returning
        # the result of __getitem__. It can be overridden to provide extra
        # values that are to be set as attributes on the new type.
        return {}

    def __getitem__(cls, item: Any) -> type:
        if getattr(cls, "_parameterized", False):
            raise NPTypingError(f"Type nptyping.{cls} is already parameterized.")

        args = cls._get_item(item)
        additional_values = cls._get_additional_values(item)
        assert hasattr(cls, "__args__"), "A SubscriptableMeta must have __args__."
        if args != cls.__args__:  # type: ignore[attr-defined]
            result = cls._create_type(args, additional_values)
        else:
            result = cls

        return result

    def _create_type(
        cls, args: Tuple[Any, ...], additional_values: Dict[str, Any]
    ) -> type:
        key = (cls, args)
        if key not in cls._all_types:
            cls._all_types[key] = type(
                cls.__name__,
                (cls,),
                {"__args__": args, "_parameterized": True, **additional_values},
            )
        return cls._all_types[key]


class ComparableByArgsMeta(ABCMeta):
    """
    Makes a class comparable by means of its __args__.
    """

    __args__: Tuple[Any, ...]

    def __eq__(cls, other: Any) -> bool:
        return (
            hasattr(cls, "__args__")
            and hasattr(other, "__args__")
            and cls.__args__ == other.__args__
        )

    def __hash__(cls) -> int:
        return hash(cls.__args__)


class ContainerMeta(
    InconstructableMeta,
    ImmutableMeta,
    FinalMeta,
    MaybeCheckableMeta,
    PrintableMeta,
    SubscriptableMeta,
    ComparableByArgsMeta,
    ABCMeta,
):
    """
    Base meta class for "containers" such as Shape and Structure.
    """

    _known_expressions: Set[str] = set()
    __args__: Tuple[str, ...]

    @abstractmethod
    def _validate_expression(cls, item: str) -> None:
        ...  # pragma: no cover

    @abstractmethod
    def _normalize_expression(cls, item: str) -> str:
        ...  # pragma: no cover

    def _get_item(cls, item: Any) -> Tuple[Any, ...]:
        if not isinstance(item, str):
            raise InvalidArgumentsError(
                f"Unexpected argument of type {type(item)}, expecting a string."
            )

        if item in cls._known_expressions:
            # No need to do costly validations and normalizations if it has been done
            # before.
            return (item,)

        cls._validate_expression(item)
        norm_shape_expression = cls._normalize_expression(item)
        cls._known_expressions.add(norm_shape_expression)
        return (norm_shape_expression,)

    def __subclasscheck__(cls, subclass: Any) -> bool:
        type_match = type(subclass) == type(  # pylint: disable=unidiomatic-typecheck
            cls
        )
        return type_match and (
            subclass.__args__ == cls.__args__ or not cls._parameterized
        )

    def __str__(cls) -> str:
        return f"{cls.__name__}['{cls.__args__[0]}']"

    def __eq__(cls, other: Any) -> bool:
        result = cls is other
        if not result and hasattr(cls, "__args__") and hasattr(other, "__args__"):
            normalized_args = tuple(
                cls._normalize_expression(str(arg)) for arg in other.__args__
            )
            result = cls.__args__ == normalized_args
        return result

    def __hash__(cls) -> int:
        return hash(cls.__args__)
