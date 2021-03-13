from typing import Any

import numpy as np

from nptyping._hashed_subscriptable_type import HashedSubscriptableType
from nptyping.types._nptype import NPType


def is_subarray_type(dtype: np.dtype) -> bool:
    """Detect if the type is a subarray."""
    return (hasattr(dtype, 'shape')
            and isinstance(dtype.shape, tuple)
            and len(dtype.shape) != 0)


class _SubArrayTypeMeta(HashedSubscriptableType):
    def __hash__(cls) -> int:
        return hash((cls.base, cls.shape))

    def __repr__(cls) -> str:
        if cls.base is not None:
            return 'SubArrayType[{0}, {1}]'.format(cls.base, cls.shape)
        return 'SubArrayType'

    def __eq__(cls, instance: Any) -> bool:
        if hasattr(instance, 'base') and hasattr(instance, 'shape'):
            return instance.base == cls.base and instance.shape == cls.shape
        return False

    def __instancecheck__(cls, instance: Any) -> bool:
        from nptyping.functions._get_type import get_type
        return (is_subarray_type(instance)
                and (cls == instance or cls == get_type(instance)))

    def __getitem__(cls, args: Any) -> None:
        from nptyping.functions._get_type import get_type

        if isinstance(args, np.dtype):
            base = get_type(args.base)
            shape = args.shape
        elif isinstance(args, tuple):
            base_raw, shape = args
            base = get_type(base_raw)
        else:
            raise Exception(
                'Incompatible arguments to SubArrayType: {}'.format(args))
        return HashedSubscriptableType.__getitem__(cls, (base, shape))

    __str__ = __repr__
    __subclasscheck__ = __eq__


class SubArrayType(NPType, metaclass=_SubArrayTypeMeta):
    """
    Corresponds to the dtype of a NumPy subarray.
    """
    base = None
    shape = None

    @classmethod
    def _after_subscription(cls, args: Any) -> None:
        cls.base, cls.shape = args
