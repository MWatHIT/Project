#-*- coding: UTF-8 -*-
"""refer  the plone.app.discussion catalog indexes
"""
import unittest2 as unittest

import transaction
from zope import event

from datetime import datetime

from zope.component import createObject
from zope.annotation.interfaces import IAnnotations

from Products.CMFCore.utils import getToolByName

from plone.app.testing import TEST_USER_ID, setRoles

from xtshzz.policy.testing import POLICY_INTEGRATION_TESTING

from dexterity.membrane import indexers as catalog
from plone.indexer.delegate import DelegatingIndexerFactory

class CatalogSetupTest(unittest.TestCase):

    layer = POLICY_INTEGRATION_TESTING
    
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))    
        self.portal = portal
        
    def test_catalog_installed(self):
        self.assertTrue('email' in
                        self.portal.portal_catalog.indexes())
        self.assertTrue('Title' in
                        self.portal.portal_catalog.indexes())
        
    def test_conversation_total_comments(self):
        self.assertTrue(isinstance(catalog.Title,
                                DelegatingIndexerFactory))
        self.assertTrue(isinstance(catalog.member_email,
                                DelegatingIndexerFactory))
        p0 = self.portal['memberfolder1']['member1']        
        p1 = self.portal['memberfolder1']['100']
        p2 = self.portal['memberfolder1']['200']
        self.assertEqual(catalog.Title(p0)(), u"tangyuejun")        
        self.assertEqual(catalog.Title(p1)(), u"tangyuejun")
        self.assertEqual(catalog.Title(p2)(), u"tangyuejun")
        self.assertEqual(catalog.member_email(p0)(), "12@qq.com")        
        self.assertEqual(catalog.member_email(p1)(), "100@qq.com")
        self.assertEqual(catalog.member_email(p2)(), "200@qq.com")                 

    def test_catalogsearch(self):   
        catalog2 = getToolByName(self.portal, 'portal_catalog')
        results2 = list(catalog2({'email': "12@qq.com"}))
        self.assertEqual(len(results2), 1)            

        results2 = list(catalog2({'email': "100@qq.com"}))
        self.assertEqual(len(results2), 1)
        results2 = list(catalog2({'Title': u"tangyuejun"}))
#        import pdb
#        pdb.set_trace()
        self.assertEqual(len(results2), 3)

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
