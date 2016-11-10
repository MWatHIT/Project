#-*- coding: UTF-8 -*-
from plone import api
from five import grok
from AccessControl import ClassSecurityInfo, getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager, setSecurityManager
from emc.memberArea.interfaces import ITodoitemWillCreateEvent
from plone.app.textfield.value import RichTextValue
#chown require plone.api
from emc.memberArea.subscribers.build_tree import chown

# from Products.PluggableAuthService.interfaces.authservice import IPropertiedUser
from zope.interface import Interface
from emc.memberArea.content.todoitem import ITodoitem
from emc.memberArea.utils import UnrestrictedUser

@grok.subscribe(ITodoitemWillCreateEvent)
def create_todoitem(event):
    """创建个人代办事项"""
# fetch parameters of the event instance    
    title = event.title
    userid = event.userid
    sender = event.sender
    sender = api.user.get(userid=sender).fullname or sender
    description = u"消息来自于：".encode("utf-8")
    description = "%s%s" % (description,sender)
    text = event.text
#     import pdb
#     pdb.set_trace()    
    todofolder = get_personal_todo_container_byid(userid)
    if todofolder is None: return
# bypass permission check
    old_sm = getSecurityManager()
    portal = api.portal.get()
    tmp_user = UnrestrictedUser(old_sm.getUser().getId(),'', ['Manager'],'')        
    tmp_user = tmp_user.__of__(portal.acl_users)
    newSecurityManager(None, tmp_user)    
# todoitem will be created in "${homefolder}/workspace/todo" container
#todoitem's id rules:fetch parent object's total,turn into string     
    
    total = str(int(getattr(todofolder, 'todoitems', '0')) + 1)
    id = '%s' % total
    todofolder.todoitems = id
#     import pdb
#     pdb.set_trace()
    todoitem = api.content.create(
                                  type="emc.memberArea.todoitem",
                                  title=title,
                                  description = description,
                                  id = id,
                                  container=todofolder)   

    todoitem.text = RichTextValue(text,'text/html','text/html')
    chown(todoitem,userid)
    # recover old sm
    setSecurityManager(old_sm)               

def get_personal_todo_container_byid(id):
    pm = api.portal.get_tool(name='portal_membership')  
    root = pm.getHomeFolder(id)
    if root is None: return None
    try:
        todofolder = root['workspace']['todo']
    except:
        return None        
    return todofolder