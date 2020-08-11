from typing import Callable
from typing import DefaultDict
from typing import TypeVar

KT = TypeVar("KT")
VT = TypeVar("VT")
T = TypeVar("T")


class ArgDefaultDict(DefaultDict[KT, VT]):
    """A defaultdict implementation which allows for using factory functions which use the missing key."""

    def __init__(self, fun_with_param: Callable[[KT], VT]):
        super().__init__(None)
        self.fun: Callable[[KT], VT] = fun_with_param

    def __missing__(self, key: KT) -> VT:
        ret: VT = self.fun(key)
        self[key] = ret
        return ret


def identity(x: T) -> T:
    """Identity function."""
    return x
