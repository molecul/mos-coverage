#!/usr/bin/env python

PROJECT = 'mos-coverage'

# Change docs/sphinx/conf.py too!
VERSION = '0.1'

from setuptools import setup, find_packages

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=VERSION,

    description='Coverage collect app for MOS',
    long_description=long_description,

    author='Alexey Galkin',
    author_email='agalkin@mirantis.com',

    url='https://github.com/molecul/mos-coverage',

    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['cliff'],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'moscov = moscov.main:main'
        ],
        'moscov.app': [
            'init = moscov.control:Init',
            'start = moscov.control:Start'
        ],
    },

    zip_safe=False,
)