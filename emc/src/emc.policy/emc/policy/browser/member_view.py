#-*- coding: UTF-8 -*-
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize
from zope import event
from Products.Five import BrowserView
from emc.theme.interfaces import IThemeSpecific

class WorkspaceUrlView(BrowserView):

    @memoize    
    def render(self):
        pm =getToolByName(self.context,'portal_membership')
        userobj = pm.getAuthenticatedMember()
        try:
            root = pm.getHomeFolder(userobj.getId())['workspace']
        except:
            root = None
        # init user workspace
        if root == None:event.notify(MemberAreaCreatedEvent(userobj))
        try:
            root = pm.getHomeFolder(userobj.getId())['workspace']
        except:
            root = None 
        if root != None:
            return root.absolute_url()
        else:
            return ""
       
       
