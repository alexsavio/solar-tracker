# Solar Tracking

[![CI](https://github.com/alexsavio/solar-tracker/actions/workflows/ci.yml/badge.svg)](https://github.com/alexsavio/solar-tracker/actions/workflows/ci.yml) [![Coverage](https://codecov.io/gh/alexsavio/solar-tracker/branch/main/graph/badge.svg?token=)](https://codecov.io/gh/alexsavio/solar-tracker)

A small Python package for calculating solar position, sunrise/sunset times, and estimating energy production for fixed-tilt panels. It includes simple geometry utilities, a `SolarPanel` helper, unit tests, and two Jupyter notebooks for visualization.

---

## 🔧 Requirements

- **Python**: >= **3.13** (as specified in `pyproject.toml`)
- Command-line tools used in this project: `just` (for task runner) and `uv` (dependency / tool runner) — both are optional but recommended. `jupyter` (Notebook/Lab) is required to open the example notebooks.


## 🚀 Quick start

1. Clone the repository:

```bash
git clone https://github.com/alexsavio/solar-tracker.git
cd solar-tracker
```

2. Install dependencies (recommended via the `Justfile` targets):

- Install all development, lint and test dependencies (default groups):

```bash
just install
```

- Install only production/runtime dependencies:

```bash
just install-prod
```

Notes:
- The `just` targets call `uv sync` and `uv run` under the hood (see `Justfile`). If you prefer not to use `just`, you can install the project in editable mode and then install development dependencies manually:

```bash
python -m pip install -e .
# then install dev/test tools listed in `pyproject.toml` dependency groups
```


## 🧩 Development workflow

- Format code:

```bash
just format
```

- Run linters and type checks:

```bash
just lint
just lint-mypy
```

- Run tests (with coverage):

```bash
just test
```

- Run a single test file or pass pytest arguments:

```bash
just test args="tests/test_main.py"
just test args="-k calculate_elevation -q"
```

- Run the package example script:

```bash
just run_main
# or
uv run python -m solar_tracking.main
```

- Build the project (using Hatch):

```bash
hatch build
```


## 📓 Notebooks

Two notebooks are included to visualize sun paths and panel behavior:

- `notebooks/sun_visualization.ipynb` — sun position visualizations
- `notebooks/panel_visualization.ipynb` — panel incidence and energy estimation visualizations

To launch the notebooks, start Jupyter Lab:

```bash
just jupyter
# or
uv run jupyter lab
```

Then open the notebook files from the Jupyter interface.


## ✅ Project structure (high level)

- `src/solar_tracking/` — implementation modules (`main.py`, `solar_panel.py`)
- `tests/` — unit tests using `pytest`
- `notebooks/` — example notebooks
- `pyproject.toml` — project metadata, dependency groups and dev tooling configuration
- `Justfile` — convenient task targets for install, format, lint, test, and running Jupyter


## 💡 Contributing

- Follow the formatting and linting rules (`just format`, `just lint`) before submitting PRs.
- Add tests for new functionality under `tests/` and run `just test` locally.
- Maintain type annotations (project uses strict `mypy` settings).

### Development checklist ✅

- Install and enable pre-commit hooks locally:

```bash
python -m pip install --upgrade pre-commit
pre-commit install
```

- Run pre-commit hooks locally on all files (useful before PRs):

```bash
pre-commit run --all-files
```

- CI: A GitHub Actions workflow (`.github/workflows/ci.yml`) runs code checks (format, ruff, mypy) and tests on push and pull requests; please make sure the workflow is passing on your branch before opening a PR.

## 📄 License

This project is released under the **MIT License** (see `pyproject.toml`).
