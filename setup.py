from setuptools import setup
from setuptools.command.install import install
from setuptools.command.build_py import build_py
import subprocess as sub
import sys
import os

setup(
    name="NISTgenerator",
    version="1.0",
    description="GDS maker",
    url="https://github.com/gregmoille/pyNISTtoolbox",
    author="Greg Moille",
    author_email="gmoille@umd.edu",
    license="Open",
    long_description="User Friendly gds maker for ring reosnators",
    packages=["NISTgenerator"],
    install_requires=[
        "numpy",
        "ipdb",
        "pandas",
        "gdspy",
        "shapely",
        "treepoem",
        "textwrap3",
    ],
    include_package_data=True,
    zip_safe=False,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved",
        "Operating System :: OS Independent",
    ),
)
