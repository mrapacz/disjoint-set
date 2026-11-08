from collections.abc import Iterator
from itertools import pairwise, product
from typing import Any

import pytest

from disjoint_set import DisjointSet, InvalidInitialMappingError


@pytest.fixture
def dset() -> DisjointSet[Any]:
    return DisjointSet()


@pytest.fixture(params=[{1: 1}, {1: 1, 2: 1, 3: 3}, {1: 2, 2: 3, 3: 4, 4: 4}])
def sample_dset(request: Any) -> DisjointSet[Any]:
    return DisjointSet(request.param)


def test_repr_evals_to_the_same_structure(sample_dset: DisjointSet[int]):
    rept_str = repr(sample_dset)

    assert eval(rept_str) == sample_dset


def test_repr_is_expected_string():
    assert repr(DisjointSet({1: 1, 2: 1})) == "DisjointSet({1: 1, 2: 1})"


@pytest.fixture()
def empty_dset() -> DisjointSet[Any]:
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
def sample_element(request: Any) -> Any:
    return request.param


def test_initializes_value_for_absent_key(
    empty_dset: DisjointSet[Any], sample_element: Any
):
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
def test_all_elements_within_sets_are_connected(
    element_sets: tuple[set[int], ...], empty_dset: DisjointSet[int]
):
    for element_set in element_sets:
        set_gen = (x for x in element_set)
        first = next(set_gen)
        for element in set_gen:
            empty_dset.union(first, element)

    for element_set in element_sets:
        for elem_a, elem_b in product(element_set, element_set):
            assert empty_dset.connected(elem_a, elem_b)
            assert empty_dset.connected(elem_b, elem_a)


def test_raises_on_invalid_init_params() -> None:
    dset: DisjointSet[int] = DisjointSet({1: 2, 2: 3})
    with pytest.raises(InvalidInitialMappingError):
        list(dset)


@pytest.mark.parametrize(
    argnames=("iterable", "expected_value"),
    argvalues=(
        pytest.param([], DisjointSet({}), id="empty list"),
        pytest.param(range(3), DisjointSet({2: 2, 1: 1, 0: 0}), id="range(3)"),
        pytest.param("abc", DisjointSet({"a": "a", "b": "b", "c": "c"}), id="string"),
    ),
)
def test_from_iterable(iterable: Any, expected_value: DisjointSet[Any]) -> None:
    assert DisjointSet.from_iterable(iterable=iterable) == expected_value


@pytest.mark.parametrize(
    "elements",
    [
        pytest.param((1, 9), id="integers"),
        pytest.param(("bob", "carol", "dave"), id="names"),
    ],
)
def test_equality_across_opposing_union_histories(elements: tuple[Any, ...]) -> None:
    left = DisjointSet()
    left.find(elements[0])
    for first, second in pairwise(elements):
        left.union(first, second)

    right = DisjointSet.from_iterable([elements[-1]])
    reversed_elements = elements[::-1]
    for first, second in pairwise(reversed_elements):
        right.union(first, second)

    expected_partition = frozenset([frozenset(elements)])
    assert frozenset(map(frozenset, left.itersets())) == expected_partition
    assert frozenset(map(frozenset, right.itersets())) == expected_partition
    assert left == right
    assert right == left


def test_equality_ignores_component_iteration_order(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class IterationOrderedSet(set[int]):
        def __init__(self, values: tuple[int, ...]) -> None:
            super().__init__(values)
            self._iteration_order = values

        def __iter__(self) -> Iterator[int]:
            return iter(self._iteration_order)

    left = DisjointSet({1: 1, 2: 1, 3: 3})
    right = DisjointSet({3: 3, 2: 2, 1: 2})
    # Equal component sets may yield their members and components in either order.
    left_blocks = [IterationOrderedSet((1, 2)), IterationOrderedSet((3,))]
    right_blocks = [IterationOrderedSet((3,)), IterationOrderedSet((2, 1))]
    assert left_blocks[0] == right_blocks[1]
    assert tuple(left_blocks[0]) != tuple(right_blocks[1])
    monkeypatch.setattr(left, "itersets", lambda: iter(left_blocks))
    monkeypatch.setattr(right, "itersets", lambda: iter(right_blocks))

    assert left == right
    assert right == left


@pytest.mark.parametrize(
    ("left_mapping", "right_mapping", "expected"),
    [
        pytest.param({}, {}, True, id="empty"),
        pytest.param({1: 1, 2: 1}, {1: 2, 2: 2}, True, id="different-roots"),
        pytest.param({1: 1, 2: 2}, {1: 2, 2: 2}, False, id="different-partitions"),
        pytest.param({1: 1}, {1: 1, 2: 2}, False, id="different-members"),
    ],
)
def test_equality_compares_partitions(
    left_mapping: dict[int, int], right_mapping: dict[int, int], expected: bool
) -> None:
    left = DisjointSet(left_mapping)
    right = DisjointSet(right_mapping)
    assert (left == right) is expected
    assert (right == left) is expected


def test_equality_with_other_type_is_false() -> None:
    assert (DisjointSet({1: 1}) == {1}) is False
