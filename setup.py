# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

def readfile(file):
    with open(file, "rt") as f:
        return f.read()


with open(os.path.join("gravity", "version.py"), "rt") as f:
    d = {}
    exec(f.read(), d, d)
    version = d["__version__"]

setup(
    name="gravity",
    version=version,
    include_package_data=True,
    packages=find_packages(),
    install_requires=readfile("requirements.txt").strip(),
    python_requires=">=3.4",
    entry_points={"console_scripts": ["gravity=gravity.__main__:cli"]},
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    zip_safe=False,
)
