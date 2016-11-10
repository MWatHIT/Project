# -*- coding: utf-8 -*-
from collective.saconnect.interfaces import ISQLAlchemyConnectionStrings
from collective.saconnect.testing import COLLECTIVE_SACONNECT_INTEGRATION_TESTING  # noqa
from Products.GenericSetup.testing import BodyAdapterTestCase
from UserDict import UserDict
from zope.component import provideAdapter
from zope.interface import directlyProvides

import unittest


TESTBODY = '''\
<?xml version="1.0"?>
<connections>
 <connection name="bar" string="eggs"/>
 <connection name="foo" string="spam"/>
</connections>
'''


class TestGS(unittest.TestCase, BodyAdapterTestCase):
    """Test that collective.saconnect is properly installed."""

    layer = COLLECTIVE_SACONNECT_INTEGRATION_TESTING

    _BODY = TESTBODY

    def setUp(self):
        self._obj = UserDict()
        directlyProvides(self._obj, ISQLAlchemyConnectionStrings)
        provideAdapter(self._getTargetClass())

    def _getTargetClass(self):
        from collective.saconnect.genericsetup import SQLAlchemyConnectionStringsXMLAdapter  # noqa
        return SQLAlchemyConnectionStringsXMLAdapter

    def _populate(self, obj):
        obj['foo'] = 'spam'
        obj['bar'] = 'eggs'

    def _verifyImport(self, obj):
        self.assertEqual(obj, dict(foo='spam', bar='eggs'))
