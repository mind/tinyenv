#!/usr/bin/env python

from setuptools import find_packages, setup

__version__ = '0.1.0'

requires = [
    'clint==0.5.1',
    'requests==2.14.2',
]

setup(
    name='tinyenv',
    version=__version__,
    description='TinyMind runtime environment helpers',
    author='TinyMind',
    author_email='hello@tinymind.ai',
    url='https://github.com/mind/tinyenv',
    packages=find_packages(),
    install_requires=requires,
)
