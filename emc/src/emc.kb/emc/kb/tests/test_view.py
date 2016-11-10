from plone.testing.z2 import Browser

import unittest
from zope import event

from emc.kb.testing import FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_ID,TEST_USER_NAME, TEST_USER_PASSWORD
from plone.app.testing import setRoles,login,logout

from emc.kb.contents.folder import Ifolder
from emc.kb.contents.kbfolder import Ikbfolder
from emc.kb.contents.ormfolder import Iormfolder


class TestView(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING
    def setUp(self):
        portal = self.layer['portal']

        setRoles(portal, TEST_USER_ID, ('Manager',))

        portal.invokeFactory('Folder', 'Members')
        portal.invokeFactory('emc.kb.folder', 'folder') 
        portal['folder'].invokeFactory('emc.kb.kbfolder', 'kbfolder')
        portal['folder'].invokeFactory('emc.kb.ormfolder', 'ormfolder')
        portal['folder']['kbfolder'].invokeFactory("File",'file',
                                            title=u"doc file",
                                            description=u"doc file")
        

        self.portal = portal

        
    def testfolderView(self):

        app = self.layer['app']
        portal = self.layer['portal']

        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
#         browser.addHeader('Authorization', 'Basic %s:%s' % ('user3', 'secret',))
        import transaction
        transaction.commit()
        browser.open(portal['folder'].absolute_url())
        
        self.assertTrue('class="pat-structure"' in browser.contents)

   
    def testkbfolderView(self):
        app = self.layer['app']
        portal = self.layer['portal']

        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
#         browser.addHeader('Authorization', 'Basic %s:%s' % ('user3', 'secret',))
        import transaction
        transaction.commit()
        browser.open(portal['folder']['kbfolder'].absolute_url())
        
        self.assertTrue('class="pat-structure"' in browser.contents)
    
    def testModelView(self):
        app = self.layer['app']
        portal = self.layer['portal']

        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
#         browser.addHeader('Authorization', 'Basic %s:%s' % ('user3', 'secret',))
        import transaction
        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        browser.open(base + "/model_listings")
        
        self.assertTrue("row table table-striped table-bordered table-condensed listing" in browser.contents)
        
