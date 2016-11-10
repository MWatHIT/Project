#-*- coding: UTF-8 -*-
from zope.interface import implementsOnly
from plone.namedfile.interfaces import INamedFileField
from plone.formwidget.namedfile.interfaces import INamedFileWidget
from plone.formwidget.namedfile.widget import  NamedFileWidget
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IFormLayer

from z3c.form.widget import FieldWidget
from zope.component import adapter
from zope.interface import implementer
from emc.theme.interfaces import IThemeSpecific  
class IFileWidget(INamedFileWidget):
    """mark interface for file upload field widget in bokeh
    """

class BokehNamedFileWidget(NamedFileWidget):
    """ file field widget for bokeh package"""
    
    implementsOnly(IFileWidget)
    
@implementer(IFieldWidget)
@adapter(INamedFileField, IThemeSpecific)
def BokehNamedFileFieldWidget(field, request):
    return FieldWidget(field, BokehNamedFileWidget(request))    
    
    