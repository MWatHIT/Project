#-*- coding: UTF-8 -*-
from plone import api
from five import grok
from AccessControl import ClassSecurityInfo, getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager, setSecurityManager
from emc.memberArea.interfaces import IMemberAreaCreatedEvent,IBackMemberAreaCreatedEvent,IMessageCreatedEvent

from zope.interface import Interface
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from emc.memberArea.content.message import IMessage
from emc.memberArea.interfaces import IWorkspace
from emc.memberArea.utils import UnrestrictedUser

def chown(context,userid):
        # Grant Ownership and Owner role to Member
    user = api.user.get(userid)
    context.changeOwnership(user)
    context.__ac_local_roles__ = None
    context.manage_setLocalRoles(userid, ['Owner'])
    context.reindexObject()    
# @grok.subscribe(IPropertiedUser,IMemberAreaCreatedEvent)
@grok.subscribe(Interface,IMemberAreaCreatedEvent)
def login_create_personal_tree(obj,event):
    """创建个人信箱"""
    pm = api.portal.get_tool(name='portal_membership')
    userid = pm.getAuthenticatedMember().getId()
    create_tree(userid)
           

@grok.subscribe(Interface,IBackMemberAreaCreatedEvent)
def Back_create_tree(obj,event):
    """创建个人信箱"""
    userid = obj.id
    create_tree(userid)    

def create_tree(userid): 
    pm = api.portal.get_tool(name='portal_membership')
    root = pm.getHomeFolder(userid)
    if root is None: return
# bypass permission check
    old_sm = getSecurityManager()
    portal = api.portal.get()

    tmp_user = UnrestrictedUser(old_sm.getUser().getId(),'', ['Manager'],'')        
    tmp_user = tmp_user.__of__(portal.acl_users)
    newSecurityManager(None, tmp_user)
#     _constrain(root, allowed_types)
  
    id = 'workspace'
    title = u'个人工作区'.encode("utf-8")
    item = api.content.create(type='emc.memberArea.workspace',id=id,title=title,container=root)
    
    chown(item,userid)
                 
    root = root['workspace']

    id = 'myfolder'
    title = u'个人网盘'.encode("utf-8")
    item = api.content.create(type='emc.memberArea.myfolder',id=id,title=title,container=root)
    chown(item,userid)
    id = 'todo'
    title = u'代办事宜'.encode("utf-8")
    item = api.content.create(type='emc.memberArea.todo',id=id,title=title,container=root)
    chown(item,userid) 
    id = 'favorite'
    title = u'我的收藏'.encode("utf-8")
    item = api.content.create(type='emc.memberArea.favorite',id=id,title=title,container=root)
    chown(item,userid)
    id = 'messagebox'
    title = u'个人信箱'.encode("utf-8")
    item = api.content.create(type='emc.memberArea.messagebox',id=id,title=title,container=root)
    chown(item,userid)
    root = root['messagebox']
    id = "inputbox"
    title = u'收件箱'.encode("utf-8")
    item = api.content.create(type='emc.memberArea.inputbox',id=id,title=title,container=root)
    chown(item,userid)
    id = "outputbox"
    title = u'发件箱'.encode("utf-8")
    item = api.content.create(type='emc.memberArea.outputbox',id=id,title=title,container=root)
    chown(item,userid)    
    # recover old sm
    setSecurityManager(old_sm)

def get_personal_inputbox_byid(obj,id):
    pm = api.portal.get_tool(name='portal_membership')
    hf = pm.getHomeFolder(id)
    if hf == None:return None
    box = hf['workspace']['messagebox']['inputbox']    
    return box

@grok.subscribe(IMessage,IMessageCreatedEvent)
def dispatch_message(obj,event):
    """This handler will deliver message to incoming box of receivers""" 
    receivers = obj.sendto
# bypass permission check
    old_sm = getSecurityManager()
    tmp_user = UnrestrictedUser(old_sm.getUser().getId(),'', ['Manager'],'')
    portal = api.portal.get()        
    tmp_user = tmp_user.__of__(portal.acl_users)
    newSecurityManager(None, tmp_user)    
    for i in receivers:
        inputbox = get_personal_inputbox_byid(obj,i)
        if inputbox == None:continue
        api.content.copy(source=obj, target=inputbox)
        id = obj.id

        # message init state is unreaded status
#         api.content.transition(obj=inputbox[id], transition='undo')
        chown(inputbox[id],i)
#         inputbox[id].reindexObject()
    # recover old sm
    setSecurityManager(old_sm)

         

