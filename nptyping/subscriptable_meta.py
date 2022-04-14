"""
MIT License

Copyright (c) 2022 Ramon Hagenaars

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
from typing import (
    Any,
    Dict,
    Tuple,
    TypeVar,
)

from nptyping.error import NPTypingError

_T = TypeVar("_T")


class SubscriptableMeta(ABCMeta):
    """
    Base meta class.

    FIXME: elaborate
    """

    _couples_cls_names_per_meta: Dict[type, str] = {}
    _all_types: Dict[Tuple[type, Tuple[Any, ...]], type] = {}
    _parameterized: bool = False

    @abstractmethod
    def _get_item(cls, item: Any) -> Tuple[Any, ...]:
        ...

    def _get_additional_values(
        cls, item: Any  # pylint: disable=unused-argument
    ) -> Dict[str, Any]:
        # This method is invoked after _get_item and right before returning
        # the result of __getitem__. It can be overridden to provide extra
        # values that are to be set as attributes on the new type.
        return {}

    def __init_subclass__(cls, cls_name: str) -> None:
        cls._couples_cls_names_per_meta[cls] = cls_name

    def __new__(cls, name: str, *args: Any, **kwargs: Any) -> type:
        if name in cls._couples_cls_names_per_meta.values():
            return type.__new__(cls, name, *args, **kwargs)

        raise NPTypingError(
            f"Cannot subclass nptyping.{cls._couples_cls_names_per_meta[cls]}."
        )

    def __call__(cls, *_: Any, **__: Any) -> None:
        raise NPTypingError(
            f"Cannot instantiate nptyping.{cls.__name__}. Did you mean to use [ ] ?"
        )

    def __setattr__(cls, key: str, value: Any) -> None:
        raise NPTypingError(f"Cannot set values to nptyping.{cls.__name__}.")

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

    def __instancecheck__(cls, instance: Any) -> bool:
        raise NPTypingError(
            f"Instance checking is not supported for nptyping.{cls.__name__}."
        )

    def __subclasscheck__(cls, subclass: Any) -> bool:
        raise NPTypingError(
            f"Subclass checking is not supported for nptyping.{cls.__name__}."
        )

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
