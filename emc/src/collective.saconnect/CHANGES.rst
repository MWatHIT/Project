Changelog
=========

2.0 (unreleased)
----------------

- Overhaul: autopep8/manual pep8, utf8-header, buildout/setup modernized
  [jensens]

1.4 (2011-10-06)
----------------

- Include CMFCore's permissions.zcml under Plone 4, so the `cmf.ManagePortal`
  permission is known.
  [hannosch]

- Fix typo that prevented z3c.saconfig support from ever being enabled.
  [elro]

1.3 (2009-05-28)
----------------

- Update z3cform dependency to plone.app.z3cform, and add include it's
  configuration in configure.zcml.
  [mj]

- Added optional support for z3c.saconfig connections; each connection
  string in collective.saconnect automatically is registered as a z3c.saconfig
  scoped session utility.
  [elro, mj]

1.2 (2009-03-20)
----------------

- Fixed adding new entries after the editing fix.
  [mj]

1.1 (2009-03-17)
----------------

- Fixed editing existing entries.
  [mj]

1.0 (2009-03-17)
----------------

- Initial release
  [mj]

