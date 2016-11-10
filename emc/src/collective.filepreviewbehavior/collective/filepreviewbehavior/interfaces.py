from zope.interface import Interface
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
import zope.component.interfaces

class IPreviewableFileCreatedEvent(zope.component.interfaces.IObjectEvent):
    """
    send the event after a previewable file has been created 
    """
class IPreviewAware( Interface ):
    """ marker interface , Behavior for enabling Products.ARFilePreview support for dexterity
        content types
    """

class IPreviewable( Interface ):
    """
    support html preview for like file content types
    """
    
    def hasPreview( ):
        """
        Has the preview
        """
    
    def setPreview( preview):
        """
        Sets the preview
        """
    
    def getPreview( ):
        """
        Get the preview
        """
   




