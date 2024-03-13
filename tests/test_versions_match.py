from pathlib import Path

import toml

import disjoint_set


def parse_pyproject_for_version() -> str:
    return toml.loads(Path("pyproject.toml").read_text())["tool"]["poetry"]["version"]


def test_versions_match():
    assert disjoint_set.__version__ == parse_pyproject_for_version()
