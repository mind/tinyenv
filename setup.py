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
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ]
)
