PHONY: dev
dev:
	uvx prek install

.PHONY: lint
lint:
	uvx prek --all-files

.PHONY: test
test:
	uv run pytest --doctest-modules --doctest-glob="*.md"
	uv run pyright

.PHONY: release
release: clean
	python setup.py sdist bdist_wheel
	echo "Checking dist:"
	twine check dist/*
	# "Are you sure you want to publish the ^ release? Press any key to continue."
	read
	twine upload dist/*

.PHONY: clean
clean:
	rm -rf build dist .coverage .mypy_cache .pytest_cache __pycache__ .tox .venv .git/hooks/pre-commit
