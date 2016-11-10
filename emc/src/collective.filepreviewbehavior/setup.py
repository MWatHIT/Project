from setuptools import setup, find_packages
import os

version = open('collective/filepreviewbehavior/version.txt').read().strip()

setup(name='collective.filepreviewbehavior',
      version=version,
      description="Dexterity behavior for file previews based on " + \
          "Products.ARFilePreview (WARNING: Archetypes dependencies!)",
      long_description=open("README.txt").read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Plone",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='dexterity behavior file preview Products.ARFilePreview ARFilePreview',
      author='Jonas Baumann, 4teamwork GmbH',
      author_email='mailto:info@4teamwork.ch',
      url='http://plone.org/products/arfilepreview/',
      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'plone.behavior',
        'Products.CMFCore',
        'Products.PortalTransforms',
        'five.grok',
        'plone.dexterity',
        'plone.directives.dexterity',
        'plone.rfc822',
        'zope.schema',
        'collective.dexteritytextindexer',
        # -*- Extra requirements: -*-
        ],
      extras_require={
          'test': ['plone.app.testing',]
          },         
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
