#!/usr/bin/env python
from distutils.core import setup

setup(
    name='rosbag_playonly',
    version='0.1',
    packages=['playonly',],
    scripts=['scripts/playonly'],
    license='BSD',
    long_description=open('README').read(),
)