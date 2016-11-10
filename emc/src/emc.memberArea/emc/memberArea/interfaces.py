#-*- coding: UTF-8 -*-
from zope.component.interfaces import IObjectEvent
from zope.interface import Interface,Attribute

class IMemberAreaCreatedEvent(IObjectEvent):
    """for current login user"""

class IBackMemberAreaCreatedEvent(IObjectEvent):
    """for back-end the user that had been created by program"""
    
class IMessageCreatedEvent(IObjectEvent):
    """for create message"""
    
class ITodoitemWillCreateEvent(Interface):
    """A event interface for 
    create a Todoitem object in the specify member's todo folder 
This is normal event (parameters event) not a object event"""
    title = Attribute("title of the todoitem ")
    userid = Attribute("userid that todoitem will be created under the user's workspace ")
    sender = Attribute("who lunch the event ")
    text = Attribute("rich text description of the todoitem ")

class IAddFavoriteEvent(IObjectEvent):
    """ Event add item favorite"""
    

    
class ISendMessageEvent(IObjectEvent):
    """ Event add item favorite"""

class IFavoriteEvent(IObjectEvent):
    """pass"""
class IUnFavoriteEvent(IObjectEvent):
    """pass"""
    
# Adapter interface for favorite functions
class IFavoriting(Interface):

        
    def number():
            """ 被多少人收藏了"""
            
    def addfavorite(userToken): 
        """add favoriter """
        
    def delfavorite(userToken): 
        """del favorite"""       

class IWorkspace(Interface):
    """Marker interface for personal root folder,using it define
    default view for root folder
    """

class IFavoritableLayer(Interface):
    """Marker interface for the Browserlayer
    """

# IFavoritable is the marker interface for contenttypes how support this behavior
class IFavoritable(Interface):
    pass

# class IFavoriting(Interface):
#     """mark interface"""
        
    
 