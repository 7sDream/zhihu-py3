#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re
import ast

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def extract_version():
    with open('zhihu/__init__.py', 'rb') as f_version:
        ast_tree = re.search(
            r'__version__ = (.*)',
            f_version.read().decode('utf-8')
        ).group(1)
        if ast_tree is None:
            raise RuntimeError('Cannot find version information')
        return str(ast.literal_eval(ast_tree))


with open('README.rst', 'rb') as f_readme:
    readme = f_readme.read().decode('utf-8')

packages = ['zhihu']

version = extract_version()

setup(
    name='zhihu-py3',
    version=version,
    keywords=['zhihu', 'network', 'spider', 'html'],
    description='Zhihu UNOFFICIAL API library in python3, '
                'with help of bs4, lxml, requests and html2text.',
    long_description=readme,

    author='7sDream',
    author_email='didislover@gmail.com',
    license='MIT',

    url='https://github.com/7sDream/zhihu-py3',
    download_url='https://github.com/7sDream/zhihu-py3',

    install_requires=[
        'beautifulsoup4',
        'requests',
        'html2text'
    ],
    extras_require={
        'lxml': ['lxml']
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
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
