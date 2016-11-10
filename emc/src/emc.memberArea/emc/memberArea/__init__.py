from zope.i18nmessageid import MessageFactory

_ = MessageFactory('emc.memberArea')

DoFavorite = 'emc.memberArea:Do favorite'
ViewFavorite = 'emc.memberArea:View favorite'
sendMessage = "emc.memberArea:Send message"
viewMessage = "emc.memberArea:View message"


from plone.behavior.interfaces import IBehaviorAssignable,IBehavior


from zope.interface import implements,Interface,alsoProvides
from zope.component import provideAdapter,adapts,queryUtility
from emc.memberArea.interfaces import IFavoriting
from emc.memberArea.content.message import IMessage
class AssignRoles(object):
    
    implements(IBehaviorAssignable)
    adapts(IMessage)
#     adapts(IFolder)    
#     adapts(IProject)    
    enabled = [IFavoriting]

    def __init__(self, context):
        self.context = context
    
    def supports(self, behavior_interface):
        return behavior_interface in self.enabled

    def enumerateBehaviors(self):
        for e in self.enabled:
            yield queryUtility(IBehavior, name=e.__identifier__)