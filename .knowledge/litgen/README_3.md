### cibuildwheel: build wheels for all platforms

[ci-buildwheel](https://cibuildwheel.readthedocs.io/en/stable/) is a tool that allows you to build wheels for all platforms.

It is configured via the [pyproject.toml](https://github.com/pthom/litgen_template/blob/main/pyproject.toml) file (see the [tool.cibuildwheel] section), and the [github workflow](https://github.com/pthom/litgen_template/blob/main/.github/workflows/wheels.yml) file.

### run_all_checks

[tools/run_all_checks.sh](https://github.com/pthom/litgen_template/blob/main/tools/run_all_checks.sh) is a script you can run before committing or pushing. It will run a collection of checks (mypy, black, ruff, pytest).
