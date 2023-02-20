import sys
from pathlib import Path

from setuptools import find_packages, setup

project_slug = "nptyping"
here = Path(__file__).parent.absolute()


def _get_dependencies(dependency_file):
    with open(here / "dependencies" / dependency_file, mode="r", encoding="utf-8") as f:
        return f.read().strip().split("\n")


# Read meta info from package_info.py.
package_info = {}
with open(here / project_slug / "package_info.py", mode="r", encoding="utf-8") as f:
    exec(f.read(), package_info)
supp_versions = package_info["__python_versions__"]

# The README.md provides the long description text.
with open("README.md", mode="r", encoding="utf-8") as f:
    long_description = f.read()

# Check the current version against the supported versions: older versions are not supported.
u_major = sys.version_info.major
u_minor = sys.version_info.minor
versions_as_ints = [[int(v) for v in version.split(".")] for version in supp_versions]
version_unsupported = not [
    1 for major, minor in versions_as_ints if u_major == major and u_minor >= minor
]
if version_unsupported:
    supported_versions_str = ", ".join(version for version in supp_versions)
    raise Exception(
        f"Unsupported Python version: {sys.version}. Supported versions: {supported_versions_str}"
    )


extras = {
    "build": _get_dependencies("build-requirements.txt"),
    "qa": _get_dependencies("qa-requirements.txt"),
    "pandas": _get_dependencies("pandas-requirements.txt"),
}
# Complete: all extras for end users, excluding dev dependencies.
extras["complete"] = [
    req for key, reqs in extras.items() for req in reqs if key not in ("build", "qa")
]
# Dev: all extras for developers, including build and qa dependencies.
extras["dev"] = [req for key, reqs in extras.items() for req in reqs]


setup(
    name=package_info["__title__"],
    version=package_info["__version__"],
    author=package_info["__author__"],
    author_email=package_info["__author_email__"],
    description=package_info["__description__"],
    url=package_info["__url__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=package_info["__license__"],
    package_data={
        "": ["*.pyi", "py.typed"],
    },
    packages=find_packages(include=("nptyping", "nptyping.*")),
    install_requires=_get_dependencies("requirements.txt"),
    extras_require=extras,
    python_requires=f">={supp_versions[0]}",
    test_suite="tests",
    zip_safe=False,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        *[f"Programming Language :: Python :: {version}" for version in supp_versions],
    ],
)
