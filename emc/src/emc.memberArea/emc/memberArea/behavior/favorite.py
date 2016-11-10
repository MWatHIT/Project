#-*- coding: UTF-8 -*-
from five import grok
from persistent.list import PersistentList
from plone.dexterity.interfaces import IDexterityContent
from emc.memberArea.events import FavoriteEvent,UnFavoriteEvent
from emc.memberArea.interfaces import IFavoriteEvent,IUnFavoriteEvent,IFavoriting
from zope.lifecycleevent.interfaces import IObjectAddedEvent,IObjectRemovedEvent
from zope.annotation.interfaces import IAnnotations
from Products.CMFCore.utils import getToolByName
from zope.component import adapter
from zope.interface import implementer
from plone.uuid.interfaces import IUUID

FAVORITE_KEY = 'emc.memberArea.favorite'

@implementer(IFavoriting)
@adapter(IDexterityContent)
class Favorite(object):
#     grok.provides(IFavoriting)
#     grok.context(IDexterityContent)
    
    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        if FAVORITE_KEY not in annotations.keys():
            # You know what happens if we don't use persistent classes here?
            annotations[FAVORITE_KEY] = PersistentList()

        self.favorite = annotations[FAVORITE_KEY]    
    
     
    def number(self):
        return len(self.favorite)
    
    def favavailable(self, userToken):
        "当前用户是否可以收藏本对象,True:可以收藏"
        return not(userToken in self.favorite)  
    
    def addfavorite(self,userToken):
        if  self.favavailable(userToken):
            self.favorite.append(userToken)
        else:
            raise KeyError("The %s is concerned about" % userToken)
    
    def delfavorite(self,userToken):
        if not self.favavailable(userToken):
            self.favorite.remove(userToken)
        else:
           raise KeyError("The %s is not concerned about" % userToken)
        

        
@grok.subscribe(IDexterityContent, IFavoriteEvent)
def DoFavorite(obj,event):
    """add the obj to my favorite"""
    
    mp = getToolByName(obj,'portal_membership')
    userobject = mp.getAuthenticatedMember()
    userid = userobject.getId()
    favoritelist = list(userobject.getProperty('myfavorite'))   

#     import pdb
#     pdb.set_trace()
#     fav = mp.getHomeFolder(userid)['workspace']['favorite']
#     favoritelist = list(getattr(fav,'myfavorite',[]))
    
    uuid = IUUID(obj,None)
    if uuid == None:return
    if not uuid in favoritelist:
        favoritelist.append(uuid)
        userobject.setProperties(myfavorite=favoritelist)
#         setattr(fav,'myfavorite',favoritelist)
#         fav.reindexObject()
        
    ada = IFavoriting(obj)
    if ada.favavailable(userid):
        ada.addfavorite(userid)

@grok.subscribe(IDexterityContent, IUnFavoriteEvent)
def UnFavoriteAnswer(obj,event):
    """del the answer from the favorite"""
    mp = getToolByName(obj,'portal_membership')
    userobject = mp.getAuthenticatedMember()
    userid = userobject.getId()
    favoritelist = list(userobject.getProperty('myfavorite'))    
#     fav = mp.getHomeFolder(userid)['workspace']['favorite']
#     favoritelist = list(getattr(fav,'myfavorite',[]))
    uuid = IUUID(obj,None)
    if uuid == None:return    
    if  uuid in favoritelist:
        favoritelist.remove(uuid)
        userobject.setProperties(myfavorite=favoritelist)
#         setattr(fav,'myfavorite',favoritelist)
        
    ada = IFavoriting(obj)
    if not ada.favavailable(userid):
        ada.delfavorite(userid)
        
@grok.subscribe(IDexterityContent, IObjectRemovedEvent)
def delFavorite(obj,event):
        
    """判断当前答案是否被收藏，当对象被删除时，收藏也应删除"""    
    
    try:
        ada = IFavoriting(obj)
    except:
        return

    useridlist = ada.favorite
    if len(useridlist) == 0:
        return
    
    mp = getToolByName(obj, 'portal_membership')
    for userid in useridlist:
        fav = mp.getHomeFolder(userid)['workspace']['favorite']
        favoritelist = list(getattr(fav,'myfavorite',[]))
        uuid = IUUID(obj)
#         """删除用户收藏到答案"""        
        if uuid in favoritelist:
            favoritelist.remove(uuid)
            setattr(fav,'myfavorite',favoritelist)


        