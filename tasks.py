"""
MIT License

Copyright (c) 2022 Ramon Hagenaars

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import os
import shutil
import sys
import venv as venv_
from glob import glob
from pathlib import Path

import invoke.tasks as invoke_tasks
from invoke import task

_ROOT = "nptyping"
_PY_VERSION_STR = (
    f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
)
_DEFAULT_VENV = f".venv{_PY_VERSION_STR}"

if sys.version_info.minor >= 11:
    # Patch invoke to replace a deprecated inspect function.
    # FIXME: https://github.com/pyinvoke/invoke/pull/877
    invoke_tasks.inspect.getargspec = invoke_tasks.inspect.getfullargspec


if os.name == "nt":
    _PY_SUFFIX = "\\Scripts\\python.exe"
    _PIP_SUFFIX = "\\Scripts\\pip.exe"
else:
    _PY_SUFFIX = "/bin/python"
    _PIP_SUFFIX = "/bin/pip"


def get_venv(py=None):
    return f".venv{py}" if py else _DEFAULT_VENV


def get_constraints(py=None):
    if py is not None:
        # Skip the patch version.
        py = ".".join(py.split(".")[:2])

    return f"constraints-{py}.txt" if py else "constraints.txt"


def get_py(py=None):
    return f"{get_venv(py)}{_PY_SUFFIX}"


def get_pip(py=None):
    return f"{get_venv(py)}{_PIP_SUFFIX}"


def get_versions(py=None):
    if py:
        py_versions = [py]
    else:
        py_versions = sorted(
            venv_path.split(".venv")[1]
            for venv_path in glob(str(Path(__file__).parent / ".venv*"))
        )
        py_versions.sort(key=lambda version: int(version.replace(".", "")))
    return py_versions


def print_header(version, function):
    print()
    print(f"[ {version} - {function.__name__} ]")


# BUILD TOOLS


@task
def run(context, command, py=None):
    """Run the given command using the venv."""
    context.run(f"{get_py(py)} {command}")


@task
def destroy(context, py=None):
    """Destroy the generated virtual environment."""
    venv_to_destroy = get_venv(py)
    print(f"Destroying {venv_to_destroy}")
    shutil.rmtree(venv_to_destroy, ignore_errors=True)


@task
def clean(context, py=None):
    """Clean up all generated stuff."""
    print("Swiping clean the project")
    try:
        os.remove(".coverage")
    except FileNotFoundError:
        ...  # No problem at all.
    shutil.rmtree(f"{_ROOT}.egg-info", ignore_errors=True)
    shutil.rmtree("dist", ignore_errors=True)
    shutil.rmtree("build", ignore_errors=True)
    shutil.rmtree(".mypy_cache", ignore_errors=True)
    shutil.rmtree(".pytest_cache", ignore_errors=True)
    shutil.rmtree("__pycache__", ignore_errors=True)


@task
def venv(context, py=None):
    """Create a new virtual environment and install all build dependencies in
    it."""
    print(f"Creating virtual environment: {_DEFAULT_VENV}")
    venv_.create(_DEFAULT_VENV, with_pip=True)
    print("Upgrading pip")
    context.run(f"{get_py(py)} -m pip install --upgrade pip")
    context.run(f"{get_pip(py)} install -r ./dependencies/build-requirements.txt")


@task
def lock(context, py=None):
    """Lock the project dependencies in a constraints file."""
    for version in get_versions(py):
        print_header(version, lock)
        context.run(
            f"{get_py(version)} -m piptools compile ./dependencies/* --output-file {get_constraints(version)} --quiet"
        )


@task
def install(context, py=None):
    """Install all dependencies (dev)."""
    for version in get_versions(py):
        print_header(version, install)
        print(f"Upgrading pip")
        context.run(f"{get_py(version)} -m pip install --upgrade pip")
        print(f"Installing dependencies into: {version}")
        print(
            f"{get_pip(version)} install .[dev] --constraint {get_constraints(version)}"
        )
        context.run(
            f"{get_pip(version)} install .[dev] --constraint {get_constraints(version)}"
        )


@task(clean, venv, lock, install)
def init(context, py=None):
    """Initialize a new dev setup."""


@task
def wheel(context, py=None):
    """Build a wheel."""
    print(f"Installing dependencies into: {_DEFAULT_VENV}")
    context.run(f"{get_py(py)} setup.py sdist")
    context.run(f"{get_pip(py)} wheel . --wheel-dir dist --no-deps")


# QA TOOLS


@task
def test(context, py=None):
    """Run the tests."""
    for version in get_versions(py):
        print_header(version, test)
        context.run(f"{get_py(version)} -m unittest discover tests")


@task
def doctest(context, py=None, verbose=False):
    """Run the doctests."""
    # Check the README.
    context.run(f"{get_py(py)} -m doctest README.md")
    context.run(f"{get_py(py)} -m doctest USERDOCS.md")

    # And check all the modules.
    for filename in glob(f"{_ROOT}/**/*.py", recursive=True):
        if verbose:
            print(f"doctesting {filename}")
        context.run(f"{get_py(py)} -m doctest {filename}")


@task
def coverage(context, py=None):
    """Run the tests with coverage."""
    for version in get_versions(py):
        print_header(version, coverage)
        context.run(f"{get_py(version)} -m coverage run -m unittest discover tests")
    context.run(f"{get_py(py)} -m coverage combine")
    context.run(f"{get_py(py)} -m coverage report")


@task
def pylint(context, py=None):
    """Run pylint for various PEP-8 checks."""
    context.run(f"{get_py(py)} -m pylint --rcfile=setup.cfg {_ROOT}")


@task
def mypy(context, py=None):
    """Run mypy for static type checking."""
    context.run(f"{get_py(py)} -m mypy {_ROOT}")


@task(doctest, pylint, mypy, coverage)
@task
def qa(context, py=None):
    """Run the linting tools."""


# FORMATTERS


@task
def black(context, check=False, py=None):
    """Run Black for formatting."""
    cmd = f"{get_py(py)} -m black {_ROOT} setup.py tasks.py tests"
    if check:
        cmd += " --check"
    context.run(cmd)


@task
def isort(context, check=False, py=None):
    """Run isort for optimizing imports."""
    cmd = f"{get_py(py)} -m isort {_ROOT} setup.py tasks.py tests"
    if check:
        cmd += " --check"
    context.run(cmd)


@task
def autoflake(context, check=False, py=None):
    """Run autoflake to remove unused imports and variables."""
    cmd = (
        f"{get_py(py)} -m autoflake {_ROOT} setup.py tasks.py tests --recursive --in-place"
        f" --remove-unused-variables --remove-all-unused-imports --expand-star-imports"
    )
    if check:
        cmd += " --check"
    context.run(cmd)


@task
def format(context, check=False, py=None):
    """Run the formatters."""
    autoflake(context, check=check, py=py)
    isort(context, check=check, py=py)
    black(context, check=check, py=py)
