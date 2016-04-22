# -*- coding: utf-8 -*-
"""
CAPE Data
============

Author : Sang Han
Year   : 2015
License: Apache 2.0
"""

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

setup(
    name='graphucsd',
    description='A Translation Tool for Humans',
    long_description='\n'.join(
        [
            open('README.md', 'rb').read().decode('utf-8')
        ]
    ),
    author='Sang Han',
    license='Apache License 2.0',
    author_email='jjangsangy@gmail.com',
    include_package_data=True,
    packages=find_packages(exclude=['*tests']),
    version='0.0.1',
    setup_requires=[],
    cmdclass={'tests': TestCommand},
    platforms='any',
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'download = caape.__main__:main'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Unix Shell',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Utilities',
    ],
)
