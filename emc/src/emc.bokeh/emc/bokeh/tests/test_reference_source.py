#-*- coding: UTF-8 -*-
from Products.CMFCore.utils import getToolByName
from plone.namedfile.file import NamedFile
from emc.bokeh.testing import FUNCTIONAL_TESTING 

from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import unittest

import os
import datetime
from plone import namedfile
from zope.intid import IntIds
from z3c.relationfield import RelationValue
from zope.intid.interfaces import IIntIds
from zope import component


def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'r')

class TestView(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))

        portal.invokeFactory('emc.bokeh.fearture', 'fearture1',
                            title="fearture1",
                            description="demo fearture",
                            source="reference")
        item = portal['fearture1']
        
        
        portal.invokeFactory('File', 'file')
        file = portal['file']
          
        data = getFile('data_template.csv').read()    


        file.file = namedfile.NamedBlobFile(data,filename=u"data_template.csv")
        intids = component.getUtility(IIntIds)
#         file.file = NamedFile()
        file_id = intids.getId(file)
#         b.rel = RelationValue(file_id)
        item.reference = RelationValue(file_id)
#         import pdb
#         pdb.set_trace()
             
        self.portal = portal     

        
    def test_view(self):

        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        obj = portal.absolute_url() + '/fearture1'        
        page = obj + '/@@view'
#        import pdb
#        pdb.set_trace()
        browser.open(page)

        outstr = '<section class="plot">'

        
        self.assertTrue(outstr in browser.contents)
        
