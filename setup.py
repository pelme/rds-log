#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='rds-log',
    version='1.0.1',
    description='A utility to download AWS RDS logs',
    author='Andreas Pelme',
    author_email='andreas@pelme.se',
    url='https://github.com/pelme/rds-log',
    packages=['_rds_log'],
    long_description=read('README.rst'),
    install_requires=[
        'boto3==1.1.2',
        'click==5.1',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.4',
    ],
    entry_points={
        'console_scripts': 'rds-log-stream=_rds_log.commands.rds_log_stream:main'
    },
)
