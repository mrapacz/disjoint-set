from __future__ import annotations

from collections import defaultdict
from typing import Any
from typing import DefaultDict
from typing import Generic
from typing import Iterator
from typing import Set
from typing import Tuple
from typing import TypeVar
from typing import Union

from disjoint_set.utils import IdentityDict

T = TypeVar("T")


class DisjointSet(Generic[T]):
    """A disjoint set data structure."""

    def __init__(self, *args, **kwargs) -> None:
        self._data: IdentityDict[T] = IdentityDict(*args, **kwargs)

    def __contains__(self, item: T) -> bool:
        return item in self._data

    def __bool__(self) -> bool:
        return bool(self._data)

    def __get__(self, element: T) -> T:
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
            classname=self.__class__.__name__, values=", ".join(str(dset) for dset in self.itersets()),
        )

    def __iter__(self) -> Iterator[Tuple[T, T]]:
        """Iterate over items and their canonical elements."""
        for key in self._data:
            yield key, self.find(key)

    def itersets(self, with_canonical_elements: bool = False) -> Iterator[Union[Set[T], Tuple[T, Set[T]]]]:
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
        element_classes: DefaultDict[T, Set[T]] = defaultdict(set)
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
        if x != self._data[x]:
            self._data[x] = self.find(self._data[x])
        return self._data[x]

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
