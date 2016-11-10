Introduction
============

collective.gtags provides Google Code style tagging for Plone. There is a
control panel that lets administrators define a vocabulary of tags, where tags
may have a "category" prefix. For example, "Department-IT" and "Department-HR"
would both be tags in the "Department" category. A tag "Important" has no
category.

The administrator may further decide whether users should be allowed to pick
non-standard tags globally (if also enabled on a per-type basis), and list
categories as required and/or unique.

zope.schema field
-----------------

This is implemented via a custom zope.schema style field:
`collective.gtags.field.Tags`. This is a sub-class of zope.schema.Set, with
custom validation. It will only work once the package is installed, since it
depends on the ITagSettings utility installed with this package to properly
function.

The field is accompanied by a default z3c.form widget, which uses jQuery and
the jQuery autocomplete widget to provide the user interface.

See `tagging.txt` in the package for a detailed doctest of the basic tags
functionality.

Behavior
--------

To use this field, you can either use the `Tags` field directly in your own
schema, or use the `collective.gtags.behaviors.ITags` behavior in a Dexterity
type or other type that supports `plone.behavior`. This behavior will place
a tags field in the "Categorization" field set and store tags in the Subject
Dublin Core metadata field, thus taking the place of the standard 'keywords'
field.

Acknowledgements
----------------

Development of this package was sponsored by Deloitte Australia
(http://deloitte.com.au).
