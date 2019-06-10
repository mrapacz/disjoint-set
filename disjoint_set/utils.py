from collections import defaultdict
from typing import TypeVar, Callable

T = TypeVar('T')


class ArgDefaultDict(defaultdict):
    def __init__(self, fun_with_param: Callable[[T], T]):
        super().__init__(None)
        self.fun: Callable[[T], T] = fun_with_param

    def __missing__(self, key: T) -> T:
        ret = self.fun(key)
        self[key] = ret
        return ret
