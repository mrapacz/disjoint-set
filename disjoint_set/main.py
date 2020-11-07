from collections import defaultdict
from typing import DefaultDict
from typing import Generic
from typing import Iterator
from typing import List
from typing import Set
from typing import Tuple
from typing import TypeVar

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

    def __eq__(self, other):
        return isinstance(other, DisjointSet) and self._data == other._data

    def __repr__(self) -> str:
        value_dict: DefaultDict[T, List[T]] = defaultdict(list)
        for key, value in self._data.items():
            value_dict[value].append(key)
        return f"{self.__class__.__name__}({dict(self)!r})"

    def __iter__(self) -> Iterator[Tuple[T, T]]:
        for key in self._data:
            yield key, self.find(key)

    def itersets(self) -> Iterator[Set[T]]:
        """
        Yield sets of connected components.

        >>> ds = DisjointSet()
        >>> ds.union(1,2)
        >>> list(ds.itersets())
        [{1, 2}]
        """
        element_classes: DefaultDict[T, Set[T]] = defaultdict(lambda: set())
        for element in self._data:
            element_classes[self.find(element)].add(element)

        yield from element_classes.values()

    def find(self, x: T) -> T:
        """
        Return the representative member of the set of connected components to which x belongs, may be x itself.

        >>> ds = DisjointSet()
        >>> ds.find(1)
        1
        >>> ds.union(1,2)
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
        :return: None
        """
        parent_x, parent_y = self.find(x), self.find(y)
        if parent_x != parent_y:
            self._data[parent_x] = parent_y

    def connected(self, x: T, y: T) -> bool:
        """
        Return True if x and y belong to the same set (i.e. they have the canonical element).

        >>> ds = DisjointSet()
        >>> ds.connected(1,2)
        False
        >>> ds.union(1,2)
        >>> ds.connected(1,2)
        True
        """
        return self.find(x) == self.find(y)
