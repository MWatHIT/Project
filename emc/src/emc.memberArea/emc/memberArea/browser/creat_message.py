#-*- coding: UTF-8 -*-
from five import grok
from zope.component import getMultiAdapter
from zope.component.hooks import getSite
from zope.globalrequest import getRequest
from zope import schema
from z3c.form.interfaces import IEditForm
from z3c.form.error import ErrorViewSnippet
from z3c.form import field, button, interfaces
from Products.CMFPlone.utils import _createObjectByType
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFPlone import PloneMessageFactory as _p

from plone.dexterity.utils import createContentInContainer
from plone.directives import form
from zope.event import notify

from emc.memberArea.events import  MessageCreatedEvent
from emc.memberArea.content.inputbox import IInputbox
from emc.memberArea.content.outputbox import IOutputbox
from emc.memberArea.content.message import IMessage
from emc.memberArea import _
from emc.theme.interfaces import IThemeSpecific

class RegistrationForm(form.SchemaForm):
    grok.name('write_message')
    grok.context(IOutputbox)
    grok.require("emc.memberArea.send_message")
    grok.layer(IThemeSpecific)    
    schema = IMessage
    ignoreContext = True
    label = _(u"send message to member")

    def update(self):
        self.request.set('disable_border', True)
        return super(RegistrationForm, self).update()
    
    def updateWidgets(self):
        super(RegistrationForm, self).updateWidgets()
#        self.widgets['privacy'].label = u''        
#        self.widgets['privacy'].mode = 'display'
#        self.widgets['privacy'].autoresize = True
        self.widgets['title'].addClass("form-control")
        self.widgets['text'].addClass("form-control")
        self.widgets['sendto'].addClass("form-control")                        

    
    def updateActions(self):

        super(RegistrationForm, self).updateActions()
        self.actions['submit'].addClass("btn-primary btn-block btn-lg")
        self.actions['cancel'].addClass("btn-default btn-block btn-lg")       
    
    @button.buttonAndHandler(_p(u"submit"))
    def submit(self, action):
        from plone import api
        current = api.user.get_current()        
        data, errors = self.extractData() 

        if errors:
            self.status = _(u"Please correct errors")
            return       
        # a simple rule for composing object id
        inc = str(int(getattr(self.context, 'registrant_increment', '0')) + 1)
        
        data['id'] = '%s_%s' % (current.id,inc)
        self.context.registrant_increment = inc
        obj = _createObjectByType("emc.memberArea.message",self.context, data['id'])

        del data['id']        
        title = data['title']
        for k, v in data.items():
            setattr(obj, k, v)
        
        obj.reindexObject()
        # notify object created event,
        #the subscriber of the event will be put message into incoming box of the receivers.

        notify(MessageCreatedEvent(obj))
        
#        urltool = getToolByName(self.context, 'portal_url')
#        portal = urltool.getPortalObject()
#        self.request.response.redirect(portal.absolute_url() + "/login_form")
        self.request.response.redirect(self.context.absolute_url())
        IStatusMessage(self.request).addStatusMessage(
                        _(u'create_message_succesful',
                          default=u"Your message:${title} has been sent.",
                          mapping={u'title': title}),
                        type='info')
        return
    
    @button.buttonAndHandler(_p(u"Cancel"))
    def cancel(self, action):

        self.request.response.redirect(self.context.absolute_url())
        return
