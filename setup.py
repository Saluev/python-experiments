import sys
import os
import glob
from distutils.core import setup

setup(
    name="experiments",
    version='0.1',
    description='Python numerical experiments engine',
    author='Tigran Saluev',
    author_email='tigran.saluev(at)gmail.com',
    url='http://github.com/Saluev/python-experiments',
    packages = ['experiments', 'experiments.computations'],
)
