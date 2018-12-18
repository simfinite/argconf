# -*- coding: utf-8 -*-

"""Setup script for argconf

Build source distribution:
python setup.py sdist

Build wheel distribution:
python setup.py bdist_wheel --universal

"""

# Note: This setup.py script follows official reference guides:
# https://packaging.python.org/tutorials/packaging-projects/
# https://packaging.python.org/guides/distributing-packages-using-setuptools/


import setuptools

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE.txt') as f:
    license = f.read()

setuptools.setup(
    name='argconf',
    version='0.0.1.dev1',
    description='Generate commandline interfaces for your Python scripts from YAML configuration files',
    long_description=readme,
    long_description_content_type='text/x-rst',
    author='Simon Schopferer',
    author_email='simonschopferer@gmx.de',
    url='https://github.com/simfinite/argconf',
    license=license,
    packages=setuptools.find_packages(exclude=['tests']),
    include_package_data=True,
    test_suite='tests',
    install_requires=['argparse', 'argcomplete', 'pyyaml'],
    tests_require=['argparse', 'pyyaml'],
    python_requires='>=2.7',
    classifiers=[
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Topic :: Software Development :: User Interfaces"
    ],
    keywords='runtime configuration commandline interface argument parsing',
    project_urls={
        'Source': 'https://github.com/simfinite/argconf',
        'Tracker': 'https://github.com/simfinite/argconf/issues',
    },
)
