from __future__ import annotations

from collections import defaultdict
from typing import Any
from typing import DefaultDict
from typing import Generic
from typing import Iterable
from typing import Iterator
from typing import TypeVar

from disjoint_set.utils import IdentityDict

T = TypeVar("T")


class InvalidInitialMappingError(RuntimeError):
    """Runtime error raised when invalid initial mapping causes the find() methods to change during iteration."""

    def __init__(
        self,
        msg=(
            "The mapping passed during ther DisjointSet initialization must have been wrong. "
            "Check that all keys are mapping to other keys and not some external values."
        ),
        *args,
        **kwargs,
    ):
        super().__init__(msg, *args, **kwargs)


class DisjointSet(Generic[T]):
    """A disjoint set data structure."""

    def __init__(self, *args, **kwargs) -> None:
        """
        Disjoint set data structure.

        The data structure can be initialized as an empty disjoint set:
        >>> DisjointSet()
        DisjointSet({})

        But it can also be instantiated from an existing mapping such as:
        >>> DisjointSet({1: 2, 2: 2})
        DisjointSet({1: 2, 2: 2})
        """
        self._data: IdentityDict[T] = IdentityDict(*args, **kwargs)

    @classmethod
    def from_iterable(cls, iterable: Iterable[T]) -> DisjointSet[T]:
        """Instantiate a DistjointSet instance by transforming each element from an interable to a canonical element."""
        return cls({x: x for x in iterable})

    def __len__(self) -> int:
        """Return the number of elements in the disjoint set."""
        return len(self._data)

    def __contains__(self, item: T) -> bool:
        """Return True if `item` is an element of the disjoint set (not necessarily a canonical one)."""
        return item in self._data

    def __bool__(self) -> bool:
        """Return True if disjoint set contains at least one element."""
        return bool(self._data)

    def __getitem__(self, element: T) -> T:
        return self.find(element)

    def __eq__(self, other: Any) -> bool:
        """
        Return True if both DistjoinSet structures are equivalent.

        This may mean that their canonical elements are different, but the sets they form are the same.
        >>> DisjointSet({1: 1, 2: 1}) == DisjointSet({1: 2, 2: 2})
        True
        """
        if not isinstance(other, DisjointSet):
            return False

        return {tuple(x) for x in self.itersets()} == {tuple(x) for x in other.itersets()}

    def __repr__(self) -> str:
        """
        Print self in a reproducible way.

        >>> DisjointSet({1: 2, 2: 2})
        DisjointSet({1: 2, 2: 2})
        """
        sets = {key: val for key, val in self}
        return f"{self.__class__.__name__}({sets})"

    def __str__(self) -> str:
        return "{classname}({values})".format(
            classname=self.__class__.__name__,
            values=", ".join(str(dset) for dset in self.itersets()),
        )

    def __iter__(self) -> Iterator[tuple[T, T]]:
        """Iterate over items and their canonical elements."""
        try:
            for key in self._data.keys():
                yield key, self.find(key)
        except RuntimeError as e:
            raise InvalidInitialMappingError() from e

    def itersets(self, with_canonical_elements: bool = False) -> Iterator[set[T] | tuple[T, set[T]]]:
        """
        Yield sets of connected components.

        If with_canonical_elements is set to True, method will yield tuples of (<canonical_element>, <set of elements>)
        >>> ds = DisjointSet()
        >>> ds.union(1,2)
        >>> list(ds.itersets())
        [{1, 2}]
        >>> list(ds.itersets(with_canonical_elements=True))
        [(2, {1, 2})]
        """
        element_classes: DefaultDict[T, set[T]] = defaultdict(set)
        for element in self._data:
            element_classes[self.find(element)].add(element)

        if with_canonical_elements:
            yield from element_classes.items()
        else:
            yield from element_classes.values()

    def find(self, x: T) -> T:
        """
        Return the canonical element of a given item.

        In case the element was not present in the data structure, the canonical element is the item itself.
        >>> ds = DisjointSet()
        >>> ds.find(1)
        1
        >>> ds.union(1, 2)
        >>> ds.find(1)
        2
        """
        while x != self._data[x]:
            self._data[x] = self._data[self._data[x]]
            x = self._data[x]
        return x

    def union(self, x: T, y: T) -> None:
        """
        Attach the roots of x and y trees together if they are not the same already.

        :param x: first element
        :param y: second element
        """
        parent_x, parent_y = self.find(x), self.find(y)
        if parent_x != parent_y:
            self._data[parent_x] = parent_y

    def connected(self, x: T, y: T) -> bool:
        """
        Return True if x and y belong to the same set (i.e. they have the canonical element).

        >>> ds = DisjointSet()
        >>> ds.connected(1, 2)
        False
        >>> ds.union(1, 2)
        >>> ds.connected(1, 2)
        True
        """
        return self.find(x) == self.find(y)
