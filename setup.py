# -*- coding: utf-8 -*-
import os
from setuptools import setup
from setuptools import find_packages
from os.path import join, abspath, normpath, dirname

with open(join(dirname(__file__), "README.rst")) as readme:
    README = readme.read()

with open(join(dirname(__file__), "VERSION")) as f:
    VERSION = f.read()

# allow setup.py to be run from any path
os.chdir(normpath(join(abspath(__file__), os.pardir)))
setup(
    name="edc-test-utils",
    version=VERSION,
    author=u"Erik van Widenfelt",
    author_email="ew2789@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    url="http://github.com/clinicedc/edc-test-model",
    license="GPL license, see LICENSE",
    description="Class and functions for tests for clinicedc/edc projects",
    long_description=README,
    zip_safe=False,
    keywords="django edc tests",
    install_requires=["model_bakery", "faker", "arrow"],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.6",
    test_suite="runtests.main",
)
