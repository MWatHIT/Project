from zope.component import queryUtility

from plone.registry.interfaces import IRegistry

from Acquisition import aq_base
from Acquisition import aq_chain
from Acquisition import aq_inner

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import IFolderish

from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.interfaces import INonStructuralFolder

from plone.app.discussion.interfaces import IDiscussionSettings
from zope.component import  queryUtility
from emc.kb.question import Iquestion

def enabled(self):
    
        context = aq_inner(self.context)

        # Fetch discussion registry
#        registry = queryUtility(IRegistry)
#        settings = registry.forInterface(IDiscussionSettings, check=False)
#
#        # Check if discussion is allowed globally
#        if not settings.globally_enabled:
#            return False

        # Always return False if object is a folder
        if (Iquestion.providedBy(context)):return True
        if (IFolderish.providedBy(context) and
            not INonStructuralFolder.providedBy(context)):
            return False

        def traverse_parents(context):
            # Run through the aq_chain of obj and check if discussion is
            # enabled in a parent folder.
            for obj in aq_chain(context):
                if not IPloneSiteRoot.providedBy(obj):
                    if (IFolderish.providedBy(obj) and
                        not INonStructuralFolder.providedBy(obj)):
                        flag = getattr(obj, 'allow_discussion', None)
                        if flag is not None:
                            return flag
            return None

        # If discussion is disabled for the object, bail out
        obj_flag = getattr(aq_base(context), 'allow_discussion', None)
        if obj_flag is False:
            return False

        # Check if traversal returned a folder with discussion_allowed set
        # to True or False.
        folder_allow_discussion = traverse_parents(context)

        if folder_allow_discussion:
            if not getattr(self, 'allow_discussion', None):
                return True
        else:
            if obj_flag:
                return True

        # Check if discussion is allowed on the content type
        portal_types = getToolByName(self, 'portal_types')
        document_fti = getattr(portal_types, context.portal_type)
        if not document_fti.getProperty('allow_discussion'):
            # If discussion is not allowed on the content type,
            # check if 'allow discussion' is overridden on the content object.
            if not obj_flag:
                return False

        return True
         
def anonymous_discussion_allowed(self):
        # Check if anonymous comments are allowed in the registry
        if self.context.portal_type in ["emc.kb.quesstion","eitoo.topic.answer","eisoo.market.hotel"]:
            return True
        
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IDiscussionSettings, check=False)
        return settings.anonymous_comments
