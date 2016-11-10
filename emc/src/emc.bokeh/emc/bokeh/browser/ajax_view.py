#-*- coding: UTF-8 -*-
from Acquisition import aq_inner
from zope.event import notify
import json
from Products.Five.browser import BrowserView
from emc.bokeh.utils import PyfileAddedEvent

class Update(BrowserView):
    "接受前台ajax 事件，更新源代码"
#     grok.name('ajaxupdate')
          

    def __call__(self):
        """

        """

        context = aq_inner(self.context)
      
        notify(PyfileAddedEvent(context))

        callback = {"result":True}
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(callback)

                  

