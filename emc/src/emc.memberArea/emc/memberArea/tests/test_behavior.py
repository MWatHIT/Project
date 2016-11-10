#-*- coding: UTF-8 -*-
import unittest
from zope import event
from zope.lifecycleevent import ObjectCreatedEvent
from plone.behavior.markers import applyMarkers

from emc.memberArea.testing import FUNCTIONAL_TESTING
from emc.memberArea.interfaces import IFavoriting,IFavoritable
from emc.memberArea.events import FavoriteEvent,UnFavoriteEvent
from zope.component import createObject
from zope.interface import alsoProvides
from zope.component import provideUtility 
from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from Products.CMFCore.utils import getToolByName

from emc.memberArea.content.messagebox import IMessagebox
from emc.memberArea.content.message import IMessage
from emc.memberArea.content.favorite import IFavorite

from plone.behavior.interfaces import IBehaviorAssignable,IBehavior
from five import grok

from zope.interface import implements,Interface,alsoProvides
from zope.component import provideAdapter,adapts,queryUtility
# from emc.memberArea.interfaces import IFavoriting

# assign the behavior to content type
class AssignRoles(object):
    
    implements(IBehaviorAssignable)
    adapts(IMessage)
#     adapts(IFolder)    
#     adapts(IProject)    
    enabled = [IFavoriting]

    def __init__(self, context):
        self.context = context
    
    def supports(self, behavior_interface):
        return behavior_interface in self.enabled

    def enumerateBehaviors(self):
        for e in self.enabled:
            yield queryUtility(IBehavior, name=e.__identifier__)

  


class TestProjectLocalRoles(unittest.TestCase):
    
    layer =  FUNCTIONAL_TESTING
        
    def test_project_LocalRoles(self):
        portal = self.layer['portal']
        app = self.layer['app']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        membership = getToolByName(portal, 'portal_membership')                
        provideAdapter(AssignRoles)
        
        portal.invokeFactory('emc.memberArea.workspace','work1')
        portal['work1'].invokeFactory('emc.memberArea.messagebox','folder1')        
        portal['work1']['folder1'].invokeFactory('emc.memberArea.outputbox','ou1')
        portal['work1']['folder1']['ou1'].invokeFactory('emc.memberArea.message','me1')
        message =  portal['work1']['folder1']['ou1']['me1']              
        import transaction
        transaction.commit()
#         alsoProvides(self.request,IFavoriteAdapter)                             
        self.assertEqual(IFavoriting(message).number(),0 )
        self.assertFalse(IFavoritable.providedBy(message))
        applyMarkers(message, ObjectCreatedEvent(message))
#         event.notify(ObjectCreatedEvent(message))
        self.assertTrue(IFavoritable.providedBy(message))        
        event.notify(FavoriteEvent(message))
        self.assertEqual(IFavoriting(message).number(),1 )       
#         