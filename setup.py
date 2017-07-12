#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


setup(
    name='bibsync',
    version='0.3.0',
    description='Merge bibtex .bib files',
    author='Joel Goop',
    author_email='joel@goop.nu',
    url='https://github.com/joelgoop/bibsync',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
    install_requires=[
        'click',
        'bibtexparser',
        'watchdog'
    ],
    entry_points={
        'console_scripts': [
            'bibsync = bibsync.main:cli',
        ]
    },
)