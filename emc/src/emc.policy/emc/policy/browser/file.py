# -*- coding: utf-8 -*-
from plone.app.contenttypes.browser.utils import Utils
from AccessControl import getSecurityManager
# from AccessControl import Unauthorized
from Products.CMFCore.permissions import ModifyPortalContent
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.MimetypesRegistry.MimeTypeItem import guess_icon_path
from plone.memoize.view import memoize
from zope.component import getMultiAdapter
from zope.interface import Interface
from zope.interface import implementer
from collective.filepreviewbehavior.interfaces import IPreviewable

class FileView(Utils):

    def __init__(self, context, request):
        super(FileView, self).__init__(context, request)

    def is_videotype(self):
        ct = self.context.file.contentType
        return 'video/' in ct

    def getSize(self):
        return self.context.file.getSize()
    
    def isKb(self):
#         import pdb
#         pdb.set_trace()
        size = self.getSize()
        if size > 1024:
            return True
        else:
            return False
        
        
    def is_audiotype(self):
        ct = self.context.file.contentType
        return 'audio/' in ct

    def get_mimetype_icon(self):
        return self.getFileMimeTypeIcon(self.context.file)
    
    def isEditable(self):
        sm = getSecurityManager()
        return sm.checkPermission(ModifyPortalContent, self.context)
    
    @memoize
    def txtgoodcode(self):
        
        data = self.context.file.data
        sourceFormats = ['cp936','utf-8']
        for format in sourceFormats:
            try:
#                 import pdb
#                 pdb.set_trace()
                return data.decode(format).encode('utf-8')
            except:
                pass
                
    @memoize
    def getFileMimeTypeIcon(self, content_file):
        context = aq_inner(self.context)
        pstate = getMultiAdapter(
            (context, self.request),
            name=u'plone_portal_state'
        )
        portal_url = pstate.portal_url()
        mtr = getToolByName(context, "mimetypes_registry")
        mime = []
        preadapter = IPreviewable(context,None)
        if preadapter !=None:              
            ftype = preadapter.getFileType()
        elif content_file.contentType:
            ftype = content_file.contentType

        if bool(ftype):
            mime.append(mtr.lookup(ftype)[0])
        if content_file.filename:
            mime.append(mtr.lookupExtension(content_file.filename))
        mime.append(mtr.lookup("application/octet-stream")[0])
        icon_paths = [m.icon_path for m in mime if hasattr(m, 'icon_path')]
        if icon_paths:
            return icon_paths[0]

        return portal_url + "/" + guess_icon_path(mime[0])            
