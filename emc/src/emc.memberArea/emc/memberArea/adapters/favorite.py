#-*- coding: UTF-8 -*-
from five import grok
from persistent.list import PersistentList
from plone.dexterity.interfaces import IDexterityContent
from emc.memberArea.events import FavoriteEvent,UnFavoriteEvent
from emc.memberArea.interfaces import IFavoriteEvent,IUnFavoriteEvent,IFavoriteAdapter
from zope.lifecycleevent.interfaces import IObjectAddedEvent,IObjectRemovedEvent
from zope.annotation.interfaces import IAnnotations
from Products.CMFCore.utils import getToolByName

FAVORITE_KEY = 'emc.memberArea.favorite'

class Answer(grok.Adapter):
    grok.provides(IFavoriteAdapter)
    grok.context(IDexterityContent)
    
    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        if FAVORITE_KEY not in annotations.keys():
            # You know what happens if we don't use persistent classes here?
            annotations[FAVORITE_KEY] = PersistentList()

        self.favorite = annotations[FAVORITE_KEY]    
    
#     
#     def __init__(self, context):
#         self.context = context        
#         annotations = IAnnotations(context)
#         self.favorite = annotations.setdefault(FAVORITE_KEY, OOSet())  
        
    def number(self):
        return len(self.favorite)
    
    def favavailable(self, userToken):
        return  (userToken in self.favorite)  
    
    def addfavorite(self,userToken):
        if not self.favavailable(userToken):
            self.favorite.append(userToken)
        else:
            raise KeyError("The %s is concerned about" % userToken)
    
    def delfavorite(self,userToken):
        if self.favavailable(userToken):
            self.favorite.remove(userToken)
        else:
           raise KeyError("The %s is not concerned about" % userToken)
        
def get_personal_favorite_byid(obj,id):
    pm = getToolByName(obj,'portal_membership')
    hf = pm.getHomeFolder(id)
    box = hf['favorite']  
    return box
        
@grok.subscribe(IDexterityContent, IFavoriteEvent)
def Favorite(obj,event):
    """add the obj to my favorite"""
    
    mp = getToolByName(obj,'portal_membership')
    userobject = mp.getAuthenticatedMember()
    userid = userobject.getId()
    fav = mp.getHomeFolder(userid)['favorite']
    favoritelist = list(fav.getattr('myfavorite',[]))
    
    if not obj.id in favoritelist:
        favoritelist.append(obj.id)
        fav.setattr(favoritelist)
#         fav.reindexObject()
        
    ada = IFavoriteAdapter(obj)
    if not ada.favavailable(userid):
        ada.addfavorite(userid)

@grok.subscribe(IDexterityContent, IUnFavoriteEvent)
def UnFavoriteAnswer(obj,event):
    """del the answer from the favorite"""
    mp = getToolByName(obj,'portal_membership')
    userobject = mp.getAuthenticatedMember()
    userid = userobject.getId()
    fav = mp.getHomeFolder(userid)['favorite']
    favoritelist = list(fav.getattr('myfavorite',[]))
    
    if  obj.id in favoritelist:
        favoritelist.remove(obj.id)
        fav.setattr(favoritelist)
        
    ada = IFavoriteAdapter(obj)
    if ada.favavailable(username):
        ada.delfavorite(username)
        
@grok.subscribe(IDexterityContent, IObjectRemovedEvent)
def delFavorite(obj,event):
    ada = IFavoriteAdapter(obj)
    """判断当前答案是否被收藏，当对象被删除时，收藏也应删除"""
    useridlist = ada.favorite
    if len(useridlist) == 0:
        return
    
    mp = getToolByName(obj, 'portal_membership')
    for userid in useridlist:
        fav = mp.getHomeFolder(userid)['favorite']
        favoritelist = list(fav.getattr('myfavorite',[]))
#         """删除用户收藏到答案"""        
        favoritelist.remove(obj.getId())
        fav.setattr(favoritelist)


        