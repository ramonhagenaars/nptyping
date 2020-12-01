from typing import Any

import numpy as np
from typish import SubscriptableType

from nptyping.types._nptype import NPType


def is_structured_type(dtype: np.dtype) -> bool:
    """Detect if the type is a structured array type."""
    return hasattr(dtype, 'fields') and dtype.fields is not None


class _StructuredTypeMeta(SubscriptableType):
    def __hash__(cls) -> int:
        return hash(cls.fields)

    def __repr__(cls) -> str:
        if cls.fields is not None:
            field_strs = ', '.join([str(f) for f in cls.fields])
            return 'StructuredType[{}]'.format(field_strs)
        return 'StructuredType'

    def __eq__(cls, instance: Any) -> bool:
        if hasattr(instance, 'fields'):
            return (instance.fields == cls.fields
                    or tuple(instance.fields) == tuple(cls.fields))
        return False

    def __instancecheck__(cls, instance: Any) -> bool:
        from nptyping.functions._get_type import get_type

        return (is_structured_type(instance)
                and (cls == instance or cls == get_type(instance)))

    __str__ = __repr__
    __subclasscheck__ = __eq__


class StructuredType(NPType, metaclass=_StructuredTypeMeta):
    """
    Corresponds to the dtype of a structured NumPy array.
    """
    fields = None

    @classmethod
    def _after_subscription(cls, args: Any) -> None:
        from nptyping.functions._get_type import get_type

        if isinstance(args, np.dtype):
            cls.fields = tuple(get_type(args.fields[n][0]) for n in args.names)
        elif isinstance(args, tuple):
            cls.fields = tuple(get_type(t) for t in args)
        elif isinstance(args, type):
            cls.fields = (get_type(args),)
        else:
            raise Exception(
                'Incompatible arguments to StructuredType: {}'.format(args))
