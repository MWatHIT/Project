from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='emc.bokeh',
      version=version,
      description="A web plot output project for EMC",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='python plone',
      author='Adam tang',
      author_email='yuejun.tang@gmail.com',
      url='https://github.com/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['emc'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'five.grok',          
          'plone.app.dexterity',
          'collective.autopermission',
          'plone.directives.form',
          'plone.directives.dexterity',          
          'plone.app.z3cform',
          'collective.z3cform.datagridfield',
          'collective.dexteritytextindexer',
          'plone.app.relationfield',
          'plone.formwidget.contenttree',                    
#          'bokeh',
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
#      setup_requires=["PasteScript"],
#      paster_plugins = ["ZopeSkel"],

      )
