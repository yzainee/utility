#!/usr/bin/env python
"""setup.py for fabric8-analytics-utils."""

from setuptools import setup, find_packages


def get_requirements():
    """Parse dependencies from 'requirements.in' file."""
    with open('requirements.in') as fd:
        lines = fd.read().splitlines()
        requires = []
        for line in lines:
            requires.append(line)
        return requires


install_requires = get_requirements()

setup(
    name='ver_utils',
    version='0.1.0',
    description='Library containing utilities and helper functions',
    install_requires=install_requires,
    license='Apache-2.0',
    author='Yusuf Zainee',
    author_email='yusufz1@verifone.com'
)
