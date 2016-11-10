.. image:: https://travis-ci.org/collective/collective.saconnect.svg?branch=master
    :target: https://travis-ci.org/collective/collective.saconnect

.. image:: https://coveralls.io/repos/collective/collective.saconnect/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/collective/collective.saconnect?branch=master


.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide_addons.html
   This text does not appear on pypi or github. It is a comment.

Introduction
============

This package provides a simple control panel and storage for `SQLAlchemy <http://www.sqlalchemy.org/>`_ connection strings.
It presents a form where one can add and remove named connections, and a GS import and export step to manage these.

This package does *not* provide SQLAlchemy integration itself;
use a library like ``zope.sqlalchemy``, ``collective.lead`` or ``pas.plugins.sqlalchemy`` instead.

Example usage:

::

    from zope.app.component.hooks import getSite
    from collective.saconnect.interfaces import ISQLAlchemyConnectionStrings

    saconnect = ISQLAlchemyConnectionStrings(getSite())
    myconnection = saconnect['myidentifier']

``ISQLAlchemyConnectionStrings`` acts as a simple dictionary, although it's keys and values must be simple strings.

To import connection strings through GenericSetup, simply include a file named saconnections.xml in your profile, with a top-level 'connections'  element and one 'connection' element per connection, with name and string attributes::

    <?xml version="1.0"?>
    <connections>
     <connection name="bar" string="sqlite:////path/to/bar.sqlite"/>
     <connection name="foo" string="oracle://username:password/tnsnamethere"/>
    </connections>

To remove any of the connections, use the 'remove' attribute::

    <?xml version="1.0"?>
    <connections>
      <connection name="bar" remove=""/>
    </connections>

If you cache your SQLAlchemy connections, you may want to listen for the IObjectModifiedEvent for ISQLAlchemyConnectionStrings.
The event includes the key of the modified string, so you can easily refresh your database connections::

    <subscriber
        handler=".mymodule.saconnectionUpdated"
        for="collective.saconnect.interfaces.ISQLAlchemyConnectionStrings
             zope.lifecycleevent.interfaces.IObjectModifiedEvent"
    />

::

    def saconnectionUpdated(connections, event):
        if 'myconnectionstring' in event.descriptions:
            getUtility(IDatabase, u'myconnection').invalidate()

Contribute
----------

If you are having issues, please let us know.

- Issue Tracker: https://github.com/collective/collective.saconnect/issues
- Source Code: https://github.com/collective/collective.saconnect

You can clone the source and submit pull requests or `get access to the github-collective <http://collective.github.com/>`_ and work directly on the project repository.
