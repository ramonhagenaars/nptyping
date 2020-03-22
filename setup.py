"""This is the installation toolset for this project."""
from setuptools import setup


with open('README.rst', 'r') as fh:
    long_description = fh.read()


setup(name='nptyping',
      version='0.3.1',
      description='Type hints for Numpy',
      long_description=long_description,
      packages=[
          'nptyping',
      ],
      install_requires=[
          'numpy',
          'typish>=1.4.0',
      ],
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
      ])
