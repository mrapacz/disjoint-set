from typing import TypeVar, Callable, DefaultDict, Generic

KT = TypeVar('KT')
VT = TypeVar('VT')


class ArgDefaultDict(DefaultDict[KT, VT]):
    def __init__(self, fun_with_param: Callable[[KT], VT]):
        super().__init__(None)
        self.fun: Callable[[KT], VT] = fun_with_param

    def __missing__(self, key: KT) -> VT:
        ret: VT = self.fun(key)
        self[key] = ret
        return ret


def identity(x: KT) -> KT:
    return x
