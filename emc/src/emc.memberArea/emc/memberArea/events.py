#-*- coding: UTF-8 -*-
from zope import interface
from zope.component.interfaces import ObjectEvent
from emc.memberArea.interfaces import IMemberAreaCreatedEvent
from emc.memberArea.interfaces import IAddFavoriteEvent
from emc.memberArea.interfaces import ISendMessageEvent,IMessageCreatedEvent,IBackMemberAreaCreatedEvent
from emc.memberArea.interfaces import IFavoriteEvent,IUnFavoriteEvent
from emc.memberArea.interfaces import ITodoitemWillCreateEvent
from zope.lifecycleevent import ObjectCreatedEvent

class MemberAreaCreatedEvent(ObjectEvent):
    interface.implements(IMemberAreaCreatedEvent)

class AddFavoriteEvent(ObjectEvent):
    interface.implements(IAddFavoriteEvent)

class SendMessageEvent(ObjectEvent):
    interface.implements(ISendMessageEvent)
 
class MessageCreatedEvent(ObjectCreatedEvent):
    interface.implements(IMessageCreatedEvent)
class BackMessageCreatedEvent(ObjectCreatedEvent):
    interface.implements(IBackMemberAreaCreatedEvent)
    
class FavoriteEvent(ObjectEvent):
    """收藏事件"""
    interface.implements(IFavoriteEvent)

class UnFavoriteEvent(ObjectEvent):
    """取消收藏事件"""    
    interface.implements(IUnFavoriteEvent)
    
class TodoitemWillCreateEvent(object):
    """todoitem envent,subscribers of the event will create a todoitem"""
    interface.implements(ITodoitemWillCreateEvent)
    
    def __init__(self,title,userid,sender,text):
        self.title = title
        self.userid = userid
        self.sender = sender
        self.text = text                     