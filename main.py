from collections import defaultdict


class DisjointSet:
    def __init__(self):
        self.data = key_dependent_dict(lambda x: x)

    def find(self, i):
        if i != self.data[i]:
            self.data[i] = self.find(self.data[i])
        return self.data[i]

    def union(self, i, j):
        pi, pj = self.find(i), self.find(j)
        if pi != pj:
            self.data[pi] = pj

    def connected(self, i, j):
        return self.find(i) == self.find(j)


class key_dependent_dict(defaultdict):
    def __init__(self, f_of_x):
        super().__init__(None)  # base class doesn't get a factory
        self.f_of_x = f_of_x  # save f(x)

    def __missing__(self, key):  # called when a default needed
        ret = self.f_of_x(key)  # calculate default value
        self[key] = ret  # and install it in the dict
        return ret
