#!/usr/bin/env python

import glob
from setuptools import setup, find_packages

setup(
    name="domovoi",
    version="1.0.5",
    url='https://github.com/kislyuk/domovoi',
    license='Apache Software License',
    author='Andrey Kislyuk',
    author_email='kislyuk@gmail.com',
    description='AWS Lambda event handler manager',
    long_description=open('README.rst').read(),
    install_requires=[
        'boto3 >= 1.4.4, < 2',
        'chalice >= 0.8.2, < 1'
    ],
    extras_require={
        ':python_version == "2.7"': ['enum34 >= 1.1.6, < 2']
    },
    packages=find_packages(exclude=['test']),
    scripts=glob.glob('scripts/*'),
    platforms=['MacOS X', 'Posix'],
    package_data={'domovoi': ['*.json']},
    zip_safe=False,
    include_package_data=True,
    test_suite='test',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
