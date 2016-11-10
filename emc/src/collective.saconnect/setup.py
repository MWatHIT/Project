# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup
import os

version = '2.0b0.dev0'

long_desc = open("README.rst").read() + "\n"
long_desc += open(os.path.join("CHANGES.rst")).read()

setup(
    name='collective.saconnect',
    version=version,
    description="Plone Control Panel for SQL Alchemy connection strings",
    long_description=long_desc,
    classifiers=[
        "Programming Language :: Python",
    ],
    keywords='sqlalchemy plone zope2',
    author='Plone Community (started by Jarn AS)',
    author_email='info@jarn.com',
    url='http://pypi.python.org/pypi/collective.saconnect',
    license='GPL',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Plone',
        'plone.app.z3cform',
        'setuptools',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            'z3c.saconfig',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
