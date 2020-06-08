#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="61Duke",
    author_email='loveweihaitong@foxmail.com',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mulan PSL v2',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
    description="On January 1, 2020, the Python 2 code base was frozen. Since that day, there has been no further "
                "backport of Python 2, which actually makes this language and runtime environment obsolete. Nick "
                "Coghlan, the core developer, explained in the FAQ, thus ending the situation of “the core "
                "development team maintains Python 2 and 3 at the same time as a reference interpreter for about 13 "
                "years”. The final version of Python 2 is currently passing the beta testing and release candidate "
                "stage, and the last production-level version of Python 2.7.18 is expected to be launched in April "
                "2020. Although most people in the Python community agree that Python needs drastic "
                "changes—especially because of the much-needed Unicode support that was already there. But many "
                "people are frustrated that Python 2 code works well. Therefore, code migration is required, "
                "and the ultimate purpose of the library is to enable automated and rapid code migration and provide "
                "automated testing. In this process, although there may be some unsatisfactory places in the code "
                "migration process, the library will continue to iterate and maintain.",
    entry_points={
        'console_scripts': [
            'auto_py2to3=auto_py2to3.cli:main',
        ],
    },
    install_requires=requirements,
    license="Mulan PSL v2",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='auto_py2to3',
    name='auto_py2to3',
    packages=find_packages(include=['auto_py2to3', 'auto_py2to3.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://gitee.com/weihaitong/auto_py2to3',
    version='0.1.0',
    zip_safe=False,
)
