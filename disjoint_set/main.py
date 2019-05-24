from collections import defaultdict

from .utils import key_dependent_dict


class DisjointSet:
    def __init__(self):
        self._data = key_dependent_dict(lambda x: x)

    def __contains__(self, item):
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

    def find(self, x):
        """
        Returns the representative member of the set to which x belongs, may be x itself.
        :param x: element
        :return: representative
        """
        if x != self._data[x]:
            self._data[x] = self.find(self._data[x])
        return self._data[x]

    def union(self, x, y):
        """
        Attaches the roots of x and y trees together if they are not the same already.
        :param x: first element
        :param y: second element
        :return: None
        """
        parent_x, parent_y = self.find(x), self.find(y)
        if parent_x != parent_y:
            self._data[parent_x] = parent_y

    def connected(self, x, y):
        """
        Returns True if x and y belong to the same tree (i.e. they have the same root), False otherwise.
        :param x: first element
        :param y: second element
        :return: bool
        """
        return self.find(x) == self.find(y)
