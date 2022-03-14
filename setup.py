import os

from setuptools import find_packages, setup


project_slug = "nptyping"
here = os.path.abspath(os.path.dirname(__file__))
package_info = {}
with open(
    os.path.join(here, project_slug, "package_info.py"), mode="r", encoding="utf-8"
) as f:
    exec(f.read(), package_info)

with open("README.md", mode="r", encoding="utf-8") as f:
    long_description = f.read()

with open(
    os.path.join(here, "dependencies", "requirements.txt"), mode="r", encoding="utf-8"
) as f:
    requirements = f.read().strip().split("\n")

with open(
    os.path.join(here, "dependencies", "dev-requirements.txt"),
    mode="r",
    encoding="utf-8",
) as f:
    dev_requirements = f.read().strip().split("\n")

with open(
    os.path.join(here, "dependencies", "build-requirements.txt"),
    mode="r",
    encoding="utf-8",
) as f:
    build_requirements = f.read().strip().split("\n")

extras = {
    "build": build_requirements,
    "dev": dev_requirements,
}
extras["complete"] = [req for reqs in extras.values() for req in reqs]


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
        "nptyping": [
            "py.typed",
            "check_shape.pyi",
            "shape_expression.pyi",
        ],
        "nptyping.classes": [
            "ndarray.pyi",
        ],
    },
    packages=find_packages(
        exclude=("tests", "tests.*", "test_resources", "test_resources.*")
    ),
    install_requires=requirements,
    extras_require=extras,
    python_requires=f'>={package_info["__python_versions__"][0]}',
    test_suite="tests",
    zip_safe=False,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        *[
            f"Programming Language :: Python :: {version}"
            for version in package_info["__python_versions__"]
        ],
    ],
)
