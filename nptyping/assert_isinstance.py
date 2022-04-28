# type: ignore
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
from typing import (
    Any,
    Optional,
    Type,
    TypeVar,
)

try:
    from typing import TypeGuard
except ImportError:  # pragma: no cover
    from typing_extensions import TypeGuard

TYPE = TypeVar("TYPE")


def assert_isinstance(
    instance: Any, cls: Type[TYPE], message: Optional[str] = None
) -> TypeGuard[TYPE]:
    """
    A TypeGuard function that is equivalent to `assert instance, cls, message`
    that hides nasty MyPy or IDE warnings.
    :param instance: the instance that is checked against cls.
    :param cls: the class
    :param message: any message that is displayed when the assert check fails.
    :return: the type of cls.
    """
    message = message or f"instance={instance!r}, cls={cls!r}"
    assert isinstance(instance, cls), message
    return True
