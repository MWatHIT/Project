#-*- coding: UTF-8 -*-
# from five import grok
from plone.memoize.instance import memoize
from zope.component import getMultiAdapter
from Products.Five.browser import BrowserView
from Products.CMFPlone.resources import add_bundle_on_request
from Products.CMFPlone.resources import add_resource_on_request
from emc.policy import _
from emc.project.content.project import IProject
from emc.project.content.projectfolder import IProjectFolder
from emc.theme.interfaces import IThemeSpecific
from emc.memberArea.content.workspace import IWorkspace

# grok.templatedir('templates')

class WorkspaceView(BrowserView):
     
    def __init__(self,context, request):
        # Each view instance receives context and request as construction parameters
        self.context = context
        self.request = request
        add_bundle_on_request(self.request, 'workspace-legacy')
        add_resource_on_request(self.request, 'iphone-style')   


    def getContext(self,id,interfc=None):
        """provide object id and interface,search this object"""
        pass
 
    def getChild(self,id):
        """provide id ,get workspace child object"""        
#         self.context  is workspace container object
# provide id ,get workspace child object
        child = getattr(self.context,id,None)
        return child
    def getGrandson(self,son,sonson):
        """provide child id and grandson id ,get workspace grandson object"""           
        child = getattr(self.context,son,None)
        if child ==None:return None
        gson = getattr(child,sonson,None)
        return gson       
        
    def geTable(self,context,view):
        """view: a organization folder object's view name
        context: the context of view request object 
        call view come from emc.memberArea browser package
        view name may be "orgnizations_administrative","orgnizations_survey"
        """
        
        fview = getMultiAdapter((context,self.request),name=view)
        # call getMemberList function output table
        # fetch 20 items roll
        return fview.getbrains(start=0,size=10,)
            
