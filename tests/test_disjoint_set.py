import pytest

from disjoint_set import DisjointSet


@pytest.fixture
def dset() -> DisjointSet:
    return DisjointSet()


# @pytest.mark.parametrize(
#     ('disjoint_set', 'expected_value'),
#     (
#             pytest.param(DisjointSet({1: 1}))
#     )
# )
# def test_contains(dset: DisjointSet):


@pytest.fixture(params=[{1: 1}, {1: 1, 2: 1, 3: 3}])
def sample_dset(request):
    return DisjointSet(request.param)


def test_repr_evals_to_the_same_structure(sample_dset):
    assert eval(repr(sample_dset)) == sample_dset


def test_repr_is_expected_string():
    assert repr(DisjointSet({1: 1, 2: 1})) == "DisjointSet({1: 1, 2: 1})"
