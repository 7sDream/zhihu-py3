#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
import os
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


def extract_requirements(filename='requirements.txt'):
    with open(filename, 'r') as fd:
        lines = fd.read().split('\n')

    # ignore comments and empty lines
    return [line for line in lines if line and not line.strip().startswith('#')]


def extract_version():
    version = ''
    with open('zhihu/__init__.py', 'r') as fd:
        version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                            fd.read(), re.MULTILINE).group(1)

    if not version:
        raise RuntimeError('Cannot find version information')

    return version


with open('README.md', 'r') as fd:
    readme = fd.read()

with open('ChangeLog.md', 'r') as fd:
    changelog = fd.read()

packages = [
    'zhihu'
]
version = extract_version()
requires = extract_requirements()


setup(
    name='zhihu-py3',
    version=version,
    description='A parser of zhihu.com with help of bs4 and requests in python3',
    long_description='{0}\n\n{1}'.format(readme, changelog),

    author='7sDream',
    author_email='didislover@gmail.com',
    license='MIT',

    url='https://github.com/7sDream/zhihu-py3',
    download_url='https://github.com/7sDream/zhihu-py3/releases',

    install_requires=requires,
    extras_require={
        'use-lxml': 'lxml'
    },
    packages=packages,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
