#-*- coding: UTF-8 -*-
from Products.CMFCore.utils import getToolByName
from emc.memberArea.testing import FUNCTIONAL_TESTING
from emc.memberArea.testing import INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles,logout
from plone.testing.z2 import Browser
import unittest

from Products.CMFCore.utils import getToolByName

class TestView(unittest.TestCase):
    
    layer = INTEGRATION_TESTING
    
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('emc.memberArea.workspace', 'work1')
        portal['work1'].invokeFactory('emc.memberArea.messagebox', 'folder1')
        portal['work1'].invokeFactory('emc.memberArea.myfolder', 'my1')
        portal['work1'].invokeFactory('emc.memberArea.todo', 'to1',title="todo items")
        portal['work1'].invokeFactory('emc.memberArea.favorite', 'fa1',title="favorite items")
        portal['work1']['to1'].invokeFactory('emc.memberArea.todoitem', 'todoitem1')                
        portal['work1']['folder1'].invokeFactory('emc.memberArea.inputbox', 'input1')
        portal['work1']['folder1'].invokeFactory('emc.memberArea.outputbox', 'output1')
        portal['work1']['folder1']['input1'].invokeFactory('emc.memberArea.message', 'message1')
        portal['work1']['folder1']['output1'].invokeFactory('emc.memberArea.message', 'message1')                      

        self.portal = portal                                
    
    def test_message_workflow(self):
        app = self.layer['app']
        portal = self.layer['portal']
        wf = getToolByName(portal, 'portal_workflow')

        wt = wf.emc_member_send_message_workflow
        dummy = portal['work1']['folder1']['input1']['message1']

        wf.notifyCreated(dummy)

        chain = wf.getChainFor(dummy)
        self.failUnless(chain[0] =='emc_member_send_message_workflow')

        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'unreaded')        
        wf.doActionFor(dummy, 'done', comment='foo' )

## available variants is actor,action,comments,time, and review_history        
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'readed')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'foo')
                 
        wf.doActionFor(dummy, 'undo', comment='undo to init')
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'unreaded')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'undo to init')        
       
    def test_todoitem_workflow(self):
        app = self.layer['app']
        portal = self.layer['portal']
        wf = getToolByName(portal, 'portal_workflow')

        wt = wf.emc_member_todoitem_workflow
        dummy = portal['work1']['to1']['todoitem1']

        wf.notifyCreated(dummy)

        chain = wf.getChainFor(dummy)

        self.failUnless(chain[0] =='emc_member_todoitem_workflow')

        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'unprocessed')        
        wf.doActionFor(dummy, 'done', comment='foo' )

## available variants is actor,action,comments,time, and review_history        
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'processed')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'foo')
                 
        wf.doActionFor(dummy, 'undo', comment='undo to init')
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'unprocessed')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'undo to init')                              



     
      
        
   