from doctest import testmod
import os
import shutil
import sys
import venv as venv_
from glob import glob
from importlib import import_module
from pathlib import Path

from invoke import task

_ROOT = "nptyping"
_PY_VERSION_STR = (
    f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
)
_DEFAULT_VENV = f".venv{_PY_VERSION_STR}"

if os.name == "nt":
    _PY_SUFFIX = "\\Scripts\\python.exe"
    _PIP_SUFFIX = "\\Scripts\\pip.exe"
else:
    _PY_SUFFIX = "/bin/python"
    _PIP_SUFFIX = "/bin/pip"


def get_venv(py=None):
    return f".venv{py}" if py else _DEFAULT_VENV


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
    print("Updating the constraints.txt")
    context.run(
        f"{get_py(py)} -m piptools compile ./dependencies/* --output-file constraints.txt --quiet"
    )


@task
def install(context, py=None):
    """Install all dependencies (complete)."""
    print(f"Installing dependencies into: {_DEFAULT_VENV}")
    context.run(f"{get_pip(py)} install .[complete] --constraint constraints.txt")


@task(clean, venv, lock, install)
def init(context, py=None):
    """Initialize a new dev setup."""


# QA TOOLS


@task
def test(context, py=None):
    """Run the tests."""
    for version in get_versions(py):
        print_header(version, test)
        context.run(f"{get_py(version)} -m unittest discover tests")


@task
def doctest(context, py=None):
    """Run the doctests."""
    # Check the README.
    context.run(f"{get_py(py)} -m doctest README.md")
    context.run(f"{get_py(py)} -m doctest USERDOCS.md")

    # And check all the modules.
    for filename in glob(f"{_ROOT}/*.py", recursive=True):
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
    cmd = f"{get_py(py)} -m black {_ROOT} setup.py tasks.py tests"
    if check:
        cmd += " --check"
    context.run(cmd)


@task
def isort(context, check=False, py=None):
    """Run isort for optimizing imports."""
    cmd = f"{get_py(py)} -m isort {_ROOT} tests"
    if check:
        cmd += " --check"
    context.run(cmd)


@task
def autoflake(context, check=False, py=None):
    """Run autoflake to remove unused imports and variables."""
    cmd = (
        f"{get_py(py)} -m autoflake {_ROOT} tests --recursive --in-place"
        f" --remove-unused-variables --expand-star-imports"
    )
    if check:
        cmd += " --check"
    context.run(cmd)


@task
def format(context, check=False, py=None):
    """Run the formatters."""
    autoflake(context, check=check)
    isort(context, check=check)
    black(context, check=check)
