# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name='spoke',
    version='0.0',
    entry_points={'console_scripts': ['spoke=spoke.cli:cli']},
    author='Valohai',
    author_email='hait@valohai.com',
    license='MIT',
    install_requires=[
        'click>=6.0',
        'requests[security]>=2.0.0',
    ],
    packages=find_packages(include=('spoke*',)),
)
