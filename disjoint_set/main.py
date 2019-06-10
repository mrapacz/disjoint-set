from collections import defaultdict
from typing import TypeVar, Generator

from disjoint_set.utils import ArgDefaultDict

T = TypeVar('T')


class DisjointSet:
    def __init__(self):
        self._data: ArgDefaultDict = ArgDefaultDict(lambda x: x)

    def __contains__(self, item: T):
        return item in self._data

    def __bool__(self):
        return bool(self._data)

    def __repr__(self):
        value_dict = defaultdict(list)
        for key, value in sorted(self._data.items()):
            value_dict[value].append(key)
        return "{classname}({values})".format(
            classname=self.__class__.__name__,
            values=', '.join([f'{key} <- {value}' for key, value in value_dict.items()]),
        )

    def __iter__(self):
        for key in self._data:
            yield key, self.find(key)

    def _refresh_labels(self) -> None:
        for item in self._data:
            self.find(item)

    def itersets(self) -> Generator[set, None, None]:
        """
        Yields sets of connected components.
        >>> ds = DisjointSet()
        >>> ds.union(1,2)
        >>> list(ds.itersets())
        [{1, 2}]
        """
        self._refresh_labels()
        element_classes: defaultdict = defaultdict(set)
        for element, element_class in self._data.items():
            element_classes[element_class].add(element)

        for element_class in element_classes.values():
            yield element_class

    def find(self, x: T) -> T:
        """
        Returns the representative member of the set of connected components to which x belongs, may be x itself.
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
        Attaches the roots of x and y trees together if they are not the same already.
        :param x: first element
        :param y: second element
        :return: None
        """
        parent_x, parent_y = self.find(x), self.find(y)
        if parent_x != parent_y:
            self._data[parent_x] = parent_y

    def connected(self, x: T, y: T) -> bool:
        """
        :param x: first element
        :param y: second element
        :return: True if x and y belong to the same tree (i.e. they have the same root), False otherwise.
        >>> ds = DisjointSet()
        >>> ds.connected(1,2)
        False
        >>> ds.union(1,2)
        >>> ds.connected(1,2)
        True
        """
        return self.find(x) == self.find(y)
