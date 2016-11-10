#-*- coding: UTF-8 -*-
from plone.dexterity.content import Item
from zope.interface import implementer
from zope.interface import Interface

class ITodoitem(Interface):
    """
    emc project member area personal todoitem content type mark interface
    """

@implementer(ITodoitem)
class Todoitem(Item):
    """Convenience subclass for ``Todoitem`` portal type
    """