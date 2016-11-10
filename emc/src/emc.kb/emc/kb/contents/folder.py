from five import grok
from plone.directives import dexterity, form
from plone.memoize.instance import memoize

from zope import schema
from Products.CMFCore.utils import getToolByName
from emc.kb import  _



# Interface class; used to define content-type schema.

class Ifolder(form.Schema):
    """
    knowledge base folder
    """
    
    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/topicfolder.xml to define the content type
    # and add directives here as necessary.




class Folder(dexterity.Container):
    grok.implements(Ifolder)
    
    # Add your class methods and properties here



