from itertools import product
from typing import Any
from typing import Set
from typing import Tuple

import pytest

from disjoint_set import DisjointSet


@pytest.fixture
def dset() -> DisjointSet:
    return DisjointSet()


@pytest.fixture(params=[{1: 1}, {1: 1, 2: 1, 3: 3}])
def sample_dset(request):
    return DisjointSet(request.param)


def test_repr_evals_to_the_same_structure(sample_dset: DisjointSet[int]):
    assert eval(repr(sample_dset)) == sample_dset


def test_repr_is_expected_string():
    assert repr(DisjointSet({1: 1, 2: 1})) == "DisjointSet({1: 1, 2: 1})"


@pytest.fixture()
def empty_dset() -> DisjointSet:
    return DisjointSet()


@pytest.fixture(
    params=[
        pytest.param("a", id="string"),
        pytest.param(1, id="int"),
        pytest.param((1, 2, 3), id="tuple"),
        pytest.param(True, id="bool"),
        pytest.param(None, id="None"),
    ]
)
def sample_element(request):
    return request.param


def test_initializes_value_for_absent_key(empty_dset: DisjointSet, sample_element: Any):
    assert sample_element not in empty_dset
    assert empty_dset.find(sample_element) == sample_element
    assert sample_element in empty_dset


@pytest.mark.parametrize(
    argnames=("element_sets",),
    argvalues=(
        pytest.param(({1, 2, 3, 6}, {4, 5}), id="variable len sets"),
        pytest.param(({1}, {2}, {3}, {4}, {5}), id="single-element sets"),
    ),
)
def test_all_elements_within_sets_are_connected(element_sets: Tuple[Set[int], ...], empty_dset: DisjointSet):
    for element_set in element_sets:
        set_gen = (x for x in element_set)
        first = next(set_gen)
        for element in set_gen:
            empty_dset.union(first, element)

    for element_set in element_sets:
        for elem_a, elem_b in product(element_set, element_set):
            assert empty_dset.connected(elem_a, elem_b)
