import unittest as unittest

from emc.memberArea.testing import INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID, setRoles
#from plone.namedfile.file import NamedImage

class Allcontents(unittest.TestCase):
    layer = INTEGRATION_TESTING
    
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('emc.memberArea.workspace', 'work1')
        portal['work1'].invokeFactory('emc.memberArea.messagebox', 'folder1')
        portal['work1'].invokeFactory('emc.memberArea.myfolder', 'my1')
        portal['work1'].invokeFactory('emc.memberArea.todo', 'to1',title="todo items")
        portal['work1'].invokeFactory('emc.memberArea.favorite', 'fa1',title="favorite items")
        portal['work1']['to1'].invokeFactory('emc.memberArea.todoitem', 'item1')
        portal['work1']['to1'].invokeFactory('emc.memberArea.todoitem', 'item2')                
        portal['work1']['folder1'].invokeFactory('emc.memberArea.inputbox', 'input1')
        portal['work1']['folder1'].invokeFactory('emc.memberArea.outputbox', 'output1')
        portal['work1']['folder1']['input1'].invokeFactory('emc.memberArea.message', 'message1')
        portal['work1']['folder1']['output1'].invokeFactory('emc.memberArea.message', 'message1')                      

        self.portal = portal
    
    def test_item_types(self):
        self.assertEqual(self.portal['work1']['folder1'].id,'folder1')
        self.assertEqual(self.portal['work1']['my1'].id,'my1')
#         import pdb
#         pdb.set_trace()
        self.assertEqual(self.portal['work1']['to1'].id,'to1')
        self.assertEqual(self.portal['work1']['to1']['item1'].id,'item1')
        self.assertEqual(self.portal['work1']['to1']['item2'].id,'item2')
        self.assertEqual(self.portal['work1']['fa1'].id,'fa1')       
        self.assertEqual(self.portal['work1']['folder1']['input1'].id,'input1') 
        self.assertEqual(self.portal['work1']['folder1']['output1'].id,'output1')                
        self.assertEqual(self.portal['work1']['folder1']['input1']['message1'].id,'message1') 
        self.assertEqual(self.portal['work1']['folder1']['output1']['message1'].id,'message1') 
        
    def test_interface(self):
        from emc.memberArea.content.messagebox import IMessagebox
        from emc.memberArea.content.message import IMessage        
        from emc.memberArea.content.inputbox import IInputbox
        from emc.memberArea.content.outputbox import IOutputbox
        from emc.memberArea.content.myfolder import IMyfolder
        from emc.memberArea.content.todo import ITodo
        from emc.memberArea.content.favorite import IFavorite                                
        self.assertTrue(IMessagebox.providedBy(self.portal['work1']['folder1']['input1']))
        self.assertTrue(IInputbox.providedBy(self.portal['work1']['folder1']['input1']))
        self.assertFalse(IMessagebox.implementedBy(self.portal['work1']['folder1']['input1']))                
        self.assertTrue(IMessagebox.providedBy(self.portal['work1']['folder1']['output1']))
        self.assertTrue(IOutputbox.providedBy(self.portal['work1']['folder1']['output1']))        
        self.assertTrue(IMessage.providedBy(self.portal['work1']['folder1']['output1']['message1']))
        self.assertTrue(IMyfolder.providedBy(self.portal['work1']['my1']))
        self.assertTrue(ITodo.providedBy(self.portal['work1']['to1']))                                         
                  
       
        