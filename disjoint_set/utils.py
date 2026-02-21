from typing import Any, TypeVar

T = TypeVar("T")


class IdentityDict(dict[T, T]):
    """A defaultdict implementation which places the requested key as its value in case it's missing."""

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

    def __missing__(self, key: T) -> T:
        self[key] = key
        return key
