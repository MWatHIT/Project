#-*- coding: UTF-8 -*-
import json
import hmac
from hashlib import sha1 as sha
from Products.CMFCore.utils import getToolByName
from emc.kb.testing import FUNCTIONAL_TESTING  

from zope.component import getUtility
from zope.interface import alsoProvides
from plone.keyring.interfaces import IKeyManager

from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import unittest
from plone.namedfile.file import NamedImage
import os

def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'r')

class TestView(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))

        portal.invokeFactory('emc.kb.folder', 'folder1',
                             title=u"this is project folder",
                             description=u"project folder")
                             
        portal['folder1'].invokeFactory('emc.kb.ormfolder', 'ormfolder',
                                        title=u"this is project",
                                        description=u"project")  

        self.portal = portal   
        
    def test_ajax_search(self):
        request = self.layer['request']
        from emc.theme.interfaces import IThemeSpecific
        alsoProvides(request, IThemeSpecific)        
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
                        '_authenticator': auth,
                        'size': '10',
                        'start':'0' ,
                        'sortcolumn':'xhdm',
                        'sortdirection':'desc',
                        'searchabletext':''                                                                       
                        }
# Look up and invoke the view via traversal
        box = self.portal['folder1']['ormfolder']
        view = box.restrictedTraverse('@@dbajaxsearch')
        result = view()
        self.assertEqual(json.loads(result)['total'],6)


                
        
     


             

