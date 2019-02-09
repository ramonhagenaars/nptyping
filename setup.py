"""This is the installation toolset for this project."""
from setuptools import setup, find_packages

with open('README.rst', 'r') as fh:
    long_description = fh.read()

setup(name='nptyping',
      version='0.2.0',
      description='Type hints for Numpy',
      long_description=long_description,
      py_modules=['nptyping'],
      install_requires=['numpy'])
