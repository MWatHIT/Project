#-*- coding: UTF-8 -*-
import unittest

from collective.filepreviewbehavior.tests.base import FUNCTIONAL_TESTING2
from collective.filepreviewbehavior.interfaces import IPreviewAware


from zope.component import createObject
from zope.interface import alsoProvides
from zope.component import provideUtility 
from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from Products.CMFCore.utils import getToolByName

from plone.app.contenttypes.interfaces import IFile


from plone.behavior.interfaces import IBehaviorAssignable,IBehavior
from five import grok

from zope.interface import implements,Interface
from zope.component import provideAdapter,adapts,queryUtility
from collective.filepreviewbehavior.interfaces import IPreviewable
from plone.dexterity.interfaces import IDexterityContent
from collective.filepreviewbehavior.tests.test_file import getFile

from zope import event
from zope.lifecycleevent import ObjectCreatedEvent
from plone.namedfile.file import NamedBlobFile
# assign the behavior to content type
class AssignRoles(object):
    
    implements(IBehaviorAssignable)
#     adapts(Interface)
    adapts(IFile)    
#     adapts(IProject)    
    enabled = [IPreviewable]

    def __init__(self, context):
        self.context = context
    
    def supports(self, behavior_interface):
        return behavior_interface in self.enabled

    def enumerateBehaviors(self):
        for e in self.enabled:
            yield queryUtility(IBehavior, name=e.__identifier__)

class Testpreviewbehavior(unittest.TestCase):
    
    layer =  FUNCTIONAL_TESTING2
      
    def test_LocalRoles(self):
        portal = self.layer['portal']
        app = self.layer['app']
        setRoles(portal, TEST_USER_ID, ('Manager',))             
        provideAdapter(AssignRoles) 
        portal.invokeFactory('File','file1')

        import transaction
        transaction.commit()
        self.assertTrue(IPreviewable(portal['file1']).key == "htmlpreview")

    def test_build_preview(self):
        portal = self.layer['portal']
        app = self.layer['app']
        setRoles(portal, TEST_USER_ID, ('Manager',))             
        provideAdapter(AssignRoles)
#         data = getFile('file.doc').read()
        import pdb
        pdb.set_trace() 
        portal.invokeFactory('File','file1')
        file = portal['file1']
#         file.file = NamedBlobFile(data, 'application/msword', 'file.doc')
        event.notify(ObjectCreatedEvent(file))
        

        import transaction
        transaction.commit()
        self.assertTrue(IPreviewable(portal['file1']).key == "htmlpreview")  
      


