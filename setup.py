import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))
meta_info = {}
with open(os.path.join(here, 'nptyping', '_meta.py'),
          mode='r', encoding='utf-8') as f:
    exec(f.read(), meta_info)

with open('README.md', mode='r', encoding='utf-8') as f:
    long_description = f.read()

requirements = [
    'numpy',
    'typish>=1.7.0',
],

test_requirements = [
    'pycodestyle',
    'pylint',
    'pytest',
    'coverage',
    'codecov',
    'scons',
    'radon',
    'xenon',
    'autoflake',
    'isort',
]

extras = {
    'test': test_requirements,
}

setup(
    name=meta_info['__title__'],
    version=meta_info['__version__'],
    author=meta_info['__author__'],
    author_email=meta_info['__author_email__'],
    description=meta_info['__description__'],
    url=meta_info['__url__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    license=meta_info['__license__'],
    packages=find_packages(exclude=('tests', 'tests.*', 'test_resources', 'test_resources.*')),
    install_requires=requirements,
    tests_require=test_requirements,
    extras_require=extras,
    python_requires='>=3.5',
    test_suite='tests',
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
