from typing import Type

from nptyping.types._nptype import NPType
from nptyping.types._number import Int, Float


def np_type(type_: type) -> Type[NPType]:
    return _NP_TYPE_PER_PY_TYPE.get(type_)


_NP_TYPE_PER_PY_TYPE = {
    int: Int,
    float: Float,
}
