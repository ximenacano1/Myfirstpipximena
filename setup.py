#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) Colav.
# Distributed under the terms of the Modified BSD License.

# -----------------------------------------------------------------------------
# Minimal Python version sanity check (from IPython)
# -----------------------------------------------------------------------------

# See https://stackoverflow.com/a/26737258/2268280
# sudo pip3 install twine
# python3 setup.py sdist bdist_wheel
# twine upload dist/*
# For test purposes
# twine upload --repository-url https://test.pypi.org/legacy/ dist/*

from __future__ import print_function
from setuptools import setup, find_packages

import os
import sys


v = sys.version_info

shell = False
if os.name in ('nt', 'dos'):
    shell = True
    warning = "WARNING: Windows is not officially supported"
    print(warning, file=sys.stderr)


def main():
    setup(
        # Application name:
        name="Myfirstpipximena",

        # Version number (initial):
        version="0.0.4",

        # Application author details:
        author="ximenacano1",
        author_email="ximena.441@gmail.co",

        # Packages
        packages=find_packages(exclude=['tests']),

        # Include additional files into the package
        include_package_data=True,

        # Details
        url="https://github.com/ximenacano1/Myfirstpipximena",
        scripts=['bin/AnomaliesXimena'],

        license="BSD",

        description="Solucion para el problema de las anomalias. Se siguen los procedimientos descritos por Costa, Dobrescu, Bogdan & Fox (2019).",

        long_description=open("README.md").read(),

        long_description_content_type="text/markdown",

        # Dependent packages (distributions)
        # See: https://github.com/pypa/pipenv/issues/2171
        install_requires=['numpy', 'pandas'],
    )


if __name__ == "__main__":
    main()
