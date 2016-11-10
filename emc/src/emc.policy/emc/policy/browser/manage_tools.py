#-*- coding: UTF-8 -*-
from zope.interface import implements
from Acquisition import aq_inner
from zope.dottedname.resolve import resolve
from zope.publisher.interfaces import IPublishTraverse
from Products.Five.browser import BrowserView
from zope.interface import Interface

from zExceptions import NotFound

class Setlayout(BrowserView):
    """
    设置指定内容对象的视图名称，通过:contentobj@@set_layout?new_view_name形式来设置。
    """    
    implements(IPublishTraverse)        
    layout = None
    #receive url parameters
    def publishTraverse(self, request, name):

        if self.layout is None:
            self.layout = name
            return self
        else:
            raise NotFound()
        
    def __call__(self):        
        obj = self.context
        try:
            obj.setLayout(self.layout)
            return "success"
        except:
            return "error"   
    
class addMarkInterface(Setlayout):
    """
    self.layout will be input a name of the mark interface ,this parameter come from browser request url
    # id is yourpackage.interfaces.IFoo
    """
    
    def __call__(self):
        ifid = self.layout
        ifobj = resolve(ifid)
        context = aq_inner(self.context)
        mark(context,Ifobj)        
        return "I has marked %s to provide %s" % (context.id,self.layout)        