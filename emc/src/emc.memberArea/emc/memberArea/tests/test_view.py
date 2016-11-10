#-*- coding: UTF-8 -*-
from Products.CMFCore.utils import getToolByName
from emc.memberArea.testing import FUNCTIONAL_TESTING 

from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import unittest as unittest
from plone.namedfile.file import NamedImage
from plone.app.textfield.value import RichTextValue
import os
import datetime

def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'r')

class TestView(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('emc.memberArea.workspace', 'work1')
        portal['work1'].invokeFactory('emc.memberArea.messagebox', 'folder1')
        portal['work1'].invokeFactory('emc.memberArea.myfolder', 'my1')
        portal['work1'].invokeFactory('emc.memberArea.todo', 'to1',title="todo container")
        portal['work1']['to1'].invokeFactory('emc.memberArea.todoitem', 'item1',
                                             title="item1",
                                             text = RichTextValue(
            u"todoitem one",
            'text/plain',
            'text/html'
        ))
        portal['work1']['to1'].invokeFactory('emc.memberArea.todoitem', 'item2',
                                             title="item2",
                                             text = RichTextValue(
            u"todoitem two",
            'text/plain',
            'text/html'
        ))      
        portal['work1'].invokeFactory('emc.memberArea.favorite', 'fa1',title="favorite items")                
        portal['work1']['folder1'].invokeFactory('emc.memberArea.inputbox', 'input1')
        portal['work1']['folder1'].invokeFactory('emc.memberArea.outputbox', 'output1')
        portal['work1']['folder1']['input1'].invokeFactory('emc.memberArea.message', 'message1')
        portal['work1']['folder1']['output1'].invokeFactory('emc.memberArea.message', 'message1')                      

        self.portal = portal  

    def test_todo_view(self):

        app = self.layer['app']
        portal = self.layer['portal']       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        obj = portal['work1']['to1'].absolute_url()       
        page = obj + '/@@view'

        browser.open(page)
        outstr = '<tr class="row" data-toggle="tooltip"'
#         import pdb
#         pdb.set_trace()        
        self.assertTrue(outstr in browser.contents)

    def test_todoitem_view(self):

        app = self.layer['app']
        portal = self.layer['portal']       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        obj = portal['work1']['to1']['item1'].absolute_url()       
        page = obj + '/@@todoitem_view'
#        import pdb
#        pdb.set_trace()
        browser.open(page)
        outstr ='todoitem one'
       
        self.assertTrue(outstr in browser.contents)

    def test_myfolder_view(self):

        app = self.layer['app']
        portal = self.layer['portal']       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        obj = portal['work1']['my1'].absolute_url()       
        page = obj + '/folder_contents'
#        import pdb
#        pdb.set_trace()
        browser.open(page)
        outstr = 'class="pat-structure"'
#         import pdb
#         pdb.set_trace()        
        self.assertTrue(outstr in browser.contents)
        
    def test_message_view(self):

        app = self.layer['app']
        portal = self.layer['portal']       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        obj = portal['work1']['folder1']['output1']['message1'].absolute_url()       
        page = obj + '/@@view'
#        import pdb
#        pdb.set_trace()
        browser.open(page)
        outstr = '<section id="content-core">'        
        self.assertTrue(outstr in browser.contents)

    def test_inputbox_view(self):        
        app = self.layer['app']
        portal = self.layer['portal']       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        obj = portal['work1']['folder1']['input1'].absolute_url()       
        page = obj + '/@@view'
#        import pdb
#        pdb.set_trace()
        browser.open(page)
        outstr = '<i class="icon-trash icon-white">'        
        self.assertTrue(outstr in browser.contents)
        
    def test_outputbox_view(self):        
        app = self.layer['app']
        portal = self.layer['portal']       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        obj = portal['work1']['folder1']['input1'].absolute_url()       
        page = obj + '/@@view'
#        import pdb
#        pdb.set_trace()
        browser.open(page)
        outstr = '<i class="icon-trash icon-white">'        
        self.assertTrue(outstr in browser.contents)
        
    def test_list_view(self):        
        app = self.layer['app']
        portal = self.layer['portal']       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        obj = portal['work1']['folder1'].absolute_url()       
        page = obj + '/@@ajax_view'
#        import pdb
#        pdb.set_trace()
        browser.open(page)
        outstr = '<div class="text-center page-header">'        
        self.assertTrue(outstr in browser.contents)
        
    def test_favorite_view(self):        
        app = self.layer['app']
        portal = self.layer['portal']       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        obj = portal['work1']['fa1'].absolute_url()
      
        page = obj + '/@@view'
#        import pdb
#        pdb.set_trace()
        browser.open(page)
        outstr = '<div class="page-header">'        
        self.assertTrue(outstr in browser.contents)                
         
    def test_sendmessage_view(self):        
        app = self.layer['app']
        portal = self.layer['portal']       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        from emc.memberArea.content.outputbox import IOutputbox
        obj = portal['work1']['folder1']['output1'] 
        self.assertTrue(IOutputbox.providedBy(obj))
#         import pdb
#         pdb.set_trace()
#          
#         page = obj.absolute_url()  + '/@@write_message'
# #        import pdb
# #        pdb.set_trace()
#         browser.open(page)
#         outstr = "send message to member"        
#         self.assertTrue(outstr in browser.contents)               