# -*- coding: utf-8 -*-
from plone.app.contenttypes.content import File
from zope.interface import Interface
from zope.interface import implementer

class ICodeFile(Interface):
    """Explicit marker interface for py code File
    """

@implementer(ICodeFile)
class CodeFile(File):
    """py code file portal type for bokeh plot generating
    """