# disjoint-set

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/disjoint_set.svg)
[![PyPI](https://img.shields.io/pypi/v/disjoint_set.svg)](https://pypi.org/project/disjoint-set/)
![Coveralls](https://img.shields.io/coveralls/github/mrapacz/disjoint-set/master.svg)
![PyPI - License](https://img.shields.io/pypi/l/disjoint_set.svg)

[DisjointSet](https://en.wikipedia.org/wiki/Disjoint-set_data_structure) (a.k.a. union–find data structure or merge–find set) implementation for Python.

## Prerequisites

The only requirement is having Python 3.8+ installed, you can verify this by running:
```bash
$ python --version
Python 3.8.16
```

## Installation
```
pip install disjoint-set
```

You can verify you're running the latest package version by running:
```python
>>> import disjoint_set
>>> disjoint_set.__version__
'0.7.4'

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

>>> list(ds)
[(1, 2), (2, 2), (3, 3), ('a', 'a')]

>>> list(ds.itersets())
[{1, 2}, {3}, {'a'}]

```

## Contributing

Feel free to open any issues on github.

## Authors

* [Maciej Rapacz](https://github.com/mrapacz/)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
