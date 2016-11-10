from zope.lifecycleevent.interfaces import IObjectAddedEvent
from plone.app.contenttypes.interfaces import IFolder
from five import grok

@grok.subscribe(IFolder,IObjectAddedEvent)
def SetLayout(obj, event):
    """ when add folder objcet in resource lib,
    set the folder layout to "folder_contents"."""
    
    path = obj.absolute_url()
    pattern = "kb_folder/resources_folder"
    default_layout = "folder_contents"
    if pattern not in path:pass
    else:
        obj.setLayout(default_layout)
    