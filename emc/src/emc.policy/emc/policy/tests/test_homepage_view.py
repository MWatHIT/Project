#-*- coding: UTF-8 -*-
from Products.CMFCore.utils import getToolByName
 
from emc.policy.testing import FunctionalTesting
from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import unittest
from plone.namedfile.file import NamedImage
from plone.namedfile.file import NamedFile
import os

def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'r')

class TestView(unittest.TestCase):
    
    layer = FunctionalTesting
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('emc.kb.folder', 'folder') 
        portal['folder'].invokeFactory('emc.kb.kbfolder', 'kbfolder')
        portal['folder']['kbfolder'].invokeFactory('File', 'f1')
        file = portal['folder']['kbfolder']
        file.file = NamedFile()
        file.title = "My File"
        file.description = "This is my file."
        
                
           
        self.portal = portal
    
    def test_homepage_view(self):

        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        obj = portal.absolute_url() + '/@@index.html'        

        browser.open(obj)
 
        outstr = "My File"
        
        self.assertTrue(outstr in browser.contents)          
        
   