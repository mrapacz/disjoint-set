from unittest import TestCase

from main import DisjointSet


class TestDisjointSet(TestCase):
    def setUp(self) -> None:
        self.dset = DisjointSet()

    def test_initializes_value_for_absent_key(self):
        self.assertEqual(
            self.dset.find(1),
            1
        )

    def test_holds_and_compares_different_data_types(self):
        values = [
            "a", 1, (1, 2, 3)
        ]

        for a, b in zip(values, values[1:]):
            self.assertEqual(
                self.dset.connected(a, b),
                False,
            )

    def test_unites_correctly(self):
        self.dset.union(1, 2)
        self.dset.union(3, 4)
        self.dset.union(1, 6)
        self.dset.union(8, 2)

        self.assertEqual(
            self.dset.connected(6, 8),
            True,
        )

        self.assertEqual(
            self.dset.connected(8, 6),
            True,
        )

    def test_finds_correctly(self):
        self.dset.union(1, 2)
        self.dset.union(2, 3)

        self.assertEqual(
            self.dset.find(3),
            3
        )

        self.assertEqual(
            self.dset.find(1),
            3
        )
