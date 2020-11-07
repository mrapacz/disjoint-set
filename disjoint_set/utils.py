from typing import Dict
from typing import TypeVar

T = TypeVar("T")


class IdentityDict(Dict[T, T]):
    """A defaultdict implementation which places the requested key as its value in case it's missing."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __missing__(self, key: T) -> T:
        self[key] = key
        return key
