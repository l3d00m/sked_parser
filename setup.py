#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = ['bs4', 'lxml', 'pyyaml', 'jsonpickle', 'requests_cache']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="l3d00m",
    author_email='substantialimpulse@pm.me',
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
    description="Parses Ostfalia sked timetables into JSON",
    entry_points={
        'console_scripts': [
            'sked-parser=sked_parser.__main__:main',
        ],
    },
    install_requires=requirements,
    package_data={
        "sked_parser": ["config.yaml"],
    },
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='sked_parser',
    name='sked_parser',
    packages=find_packages(include=['sked_parser', 'sked_parser.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/l3d00m/sked_parser',
    version='0.1.0',
    zip_safe=False,
)
