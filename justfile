# Show the version of the project
version:
  hatch version

# Install the dependencies necessary for CI and development
install:
  uv sync

# Install the dependencies needed for a production installation
install-prod:
  uv sync --no-default-groups

# Upgrade the dependencies to the latest accepted versions
upgrade:
  uv lock --upgrade

# Audit dependencies for vulnerabilities
audit:
  uv export --no-emit-project --format requirements-txt --output-file requirements.txt
  uv tool run pip-audit --no-deps --disable-pip -r requirements.txt
  rm requirements.txt

# Delete all intermediate files
clean-temp: clean-build clean-pyc

# Delete all intermediate files and caches
clean-all: clean-temp clean-caches

# Delete the Python build files and folders
clean-build:
  rm -fr build/
  rm -fr dist/
  rm -fr *.egg-info
  rm -fr *.spec

# Delete the Python intermediate execution files
clean-pyc:
  find . -name '*~' -exec rm -f {} +
  find . -name '*.log*' -delete
  find . -name '*_cache' -exec rm -rf {} +
  find . -name '*.egg-info' -exec rm -rf {} +
  find . -name '*.pyc' -exec rm -f {} +
  find . -name '*.pyo' -exec rm -f {} +
  find . -name '__pycache__' -exec rm -rf {} +

# Delete the and test caches
clean-caches:
  rm -rf .coverage
  rm -rf .pytest_cache
  rm -rf .mypy_cache
  rm -rf .files

##@ Code check

# Format your code
format:
  uv run ruff format .

# Run mypy check
lint-mypy:
  uv run mypy .

# Run ruff lint check
lint-ruff:
  uv run ruff check --fix .

# Run all code checks
lint: lint-ruff lint-mypy

# Run tests with coverage
test args="":
  uv run pytest -vvv {{args}}

# Run tests in debug mode
test-dbg args="":
  uv run pytest --pdb --ff {{args}}

# Re-run last failed tests
test-last-failed:
  uv run pytest --last-failed -vvv

# Run format, linting, then tests
check: format lint test
