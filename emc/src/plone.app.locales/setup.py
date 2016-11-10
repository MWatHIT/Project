from setuptools import setup, find_packages

version = '5.0.8.dev0'

setup(name='plone.app.locales',
      version=version,
      description="Translation files for Plone",
      long_description=open("README.rst").read() + "\n" +
                       open("CHANGES.rst").read(),
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Zope2",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
        ],
      keywords='plone i18n locale translation',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='https://github.com/collective/plone.app.locales',
      license='GPL version 2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone', 'plone.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      )
