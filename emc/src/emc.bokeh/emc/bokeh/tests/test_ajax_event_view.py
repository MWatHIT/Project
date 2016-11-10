#-*- coding: UTF-8 -*-
import json
import hmac
from hashlib import sha1 as sha
from Products.CMFCore.utils import getToolByName
from emc.bokeh.testing import INTEGRATION_TESTING,FUNCTIONAL_TESTING 


from zope.component import getUtility
from plone.keyring.interfaces import IKeyManager

from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import  unittest
from plone.namedfile.file import NamedBlobFile
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

        portal.invokeFactory('emc.bokeh.codefile', 'codefile',
                             title="codefile",description="codefile for test")     
     

        data = getFile("temp.py")
        portal['codefile'].file =  NamedBlobFile(data,"application/x-python-code",u"file.doc")                       
         
        self.portal = portal
        
                  
        
    def test_ajax_search(self):
        request = self.layer['request']        
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
                        '_authenticator': auth,
                        'subject': "ok",                                                                       
                        }
# Look up and invoke the view via traversal
        view = self.portal['codefile'].restrictedTraverse('@@ajaxupdate')
        result = view()


        self.assertEqual(json.loads(result)['result'],True)

 
