from typish import SubscriptableType


class NPType:
    """
    The baseclass of all nptyping types.
    """


class SimpleNPTypeMeta(SubscriptableType):
    """
    A metaclass for all simple NPTypes (e.g. float, int, etc.).
    """
    def __repr__(cls):
        repr_args = getattr(cls, '_repr_args', None)
        if not repr_args:
            return cls.__name__
        return '{}[{}]'.format(cls.__name__, repr_args)

    __str__ = __repr__
