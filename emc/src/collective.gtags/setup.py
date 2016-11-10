from setuptools import setup, find_packages
import os

version = '1.0b2'

setup(name='collective.gtags',
      version=version,
      description="Google Code like tagging for Plone",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Martin Aspeli',
      author_email='optilude@gmail.com',
      url='http://pypi.python.org/pypi/collective.gtags',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Plone',
          'plone.behavior>=1.0b5',
          'plone.registry>=1.0a2',
          'plone.app.registry>=1.0a2',
          'plone.z3cform',
          'z3c.form',
          'plone.directives.form>=1.0b3',
          'zope.schema',
          'zope.interface',
          'zope.component',
          'rwproperty',
      ],
      extras_require={
          'test': ['plone.app.testing',]
      },      
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
