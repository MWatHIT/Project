# encoding=utf-8
from plone.app.layout.viewlets import common as base
from Products.CMFCore.permissions import ViewManagementScreens
from Products.CMFCore.utils import getToolByName
from collective.filepreviewbehavior.interfaces import IPreviewable
from collective.filepreviewbehavior.interfaces import IPreviewAware


class FilePreview(base.ViewletBase):

    previewer = None
    preview = None


    # Update methods are guaranteed to be called before rendering for
    # Viewlets and Portlets (Because they are IContentProvider objects)
    # and for z3c.forms and formlib forms. But *not* for normal Browser Pages
    def update(self):
        super(FilePreview, self).update()

        if self.previewer is None:
            self.previewer = IPreviewable(self.context)
            self.preview = self.previewer.getPreview()
    
    def render(self):
        """ Render the viewlet only if context has preview.

        """

        # Perform some condition check
        if self.hasPreview():
            # Call parent method which performs the actual rendering
            return super(FilePreview, self).render()
        else:
            # No output when the viewlet is disabled
            return ""


    def hasPreview(self):
        "has preview content?"
        content_type = self.previewer.getFileType()
#         import pdb
#         pdb.set_trace()
        isplaintext = content_type.startswith('text')
        
        return not isplaintext and self.previewer.hasPreview() and bool(self.preview)


