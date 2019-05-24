# disjoint-set

![PyPI - License](https://img.shields.io/pypi/l/disjoint_set.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/disjoint_set.svg)
[![PyPI](https://img.shields.io/pypi/v/disjoint_set.svg)](https://pypi.org/project/disjoint-set/)

[DisjointSet](https://en.wikipedia.org/wiki/Disjoint-set_data_structure) (a.k.a. union–find data structure or merge–find set) implementation for Python.

## Prerequisites

The only requirement is having Python 3 installed, you can verify this by running:
```bash
$ python --version
Python 3.7.2
```

## Installation

```
pip install disjoint-set
```

You can verify he package was installed to your current environment by running:
```bash
$ pip list | grep disjoint-set
disjoint-set      0.5.0
```

## Usage

```python
>>> from disjoint_set import DisjointSet
>>> ds = DisjointSet()
>>> ds.find(1)
1
>>> ds.union(1,2)
>>> ds.find(1)
2
>>> ds.find(2)
2
>>> ds.connected(1,2)
True
>>> ds.connected(1,3)
False

>>> "a" in ds
False
>>> ds.find("a")
'a'
>>> "a" in ds
True

>>> list(self.dset)
[(1, 2), (2, 2), (3, 3), ('a', 'a')]
```

## Contributing

Feel free to open any issues on github.

## Authors

* [Maciej Rapacz](https://github.com/mrapacz/)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
