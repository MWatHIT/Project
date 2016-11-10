#-*- coding: UTF-8 -*-
import json
import hmac
from hashlib import sha1 as sha
from Products.CMFCore.utils import getToolByName
from xtshzz.policy.testing import POLICY_INTEGRATION_TESTING,FunctionalTesting

from zope.component import getUtility
from plone.keyring.interfaces import IKeyManager 

from plone.app.testing import TEST_USER_ID, login, logout, TEST_USER_NAME, \
    TEST_USER_PASSWORD,SITE_OWNER_NAME,SITE_OWNER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import unittest2 as unittest
from plone.namedfile.file import NamedImage

import os

def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'r')

class TestView(unittest.TestCase):   

    layer = FunctionalTesting
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        import datetime
#        import pdb
#        pdb.set_trace()
        start = datetime.datetime.today()
        end = start + datetime.timedelta(7)
        portal.invokeFactory('dexterity.membrane.memberfolder', 'memberfolder1')
        
        portal['memberfolder1'].invokeFactory('dexterity.membrane.organizationmember', 'member1',
                             email="12@qq.com",
                             last_name=u"唐",
                             first_name=u"岳军",
                             title = u"tangyuejun",
                             password="391124",
                             confirm_password ="391124",
                             homepae = 'http://315ok.org/',

                             description="I am member1")     
        portal['memberfolder1'].invokeFactory('dexterity.membrane.organizationmember', 'member2',
                             email="13@qq.com",
                             last_name=u"唐",
                             first_name=u"岳军",
                             title = u"tangyuejun",
                             password="391124",
                             confirm_password ="391124",
                             homepae = 'http://315ok.org/',

                             description="I am member1")   
        
        portal['memberfolder1'].invokeFactory('dexterity.membrane.organizationmember', 'member3',
                             email="14@qq.com",
                             last_name=u"唐",
                             first_name=u"岳军",
                             title = u"tangyuejun",
                             password="391124",
                             confirm_password ="391124",
                             homepae = 'http://315ok.org/',

                             description="I am member1")   
        
        portal['memberfolder1'].invokeFactory('dexterity.membrane.organizationmember', 'member4',
                             email="15@qq.com",
                             last_name=u"唐",
                             first_name=u"岳军",
                             title = u"tangyuejun",
                             password="391124",
                             confirm_password ="391124",
                             homepae = 'http://315ok.org/',

                             description="I am member1")   
        
        portal['memberfolder1'].invokeFactory('dexterity.membrane.organizationmember', 'member5',
                             email="16@qq.com",
                             last_name=u"唐",
                             first_name=u"岳军",
                             title = u"tangyuejun",
                             password="391124",
                             confirm_password ="391124",
                             homepae = 'http://315ok.org/',

                             description="I am member1")                                
          
 
        data = getFile('image.jpg').read()
        item = portal['memberfolder1']['member1']
        item.photo = NamedImage(data, 'image/jpg', u'image.jpg')
           
        self.portal = portal
        import transaction
        transaction.commit()
            
    def test_member_view(self):

        app = self.layer['app']
        portal = self.portal
        wf = getToolByName(portal, 'portal_workflow')

        wt = wf.dexterity_membrane_workflow
        dummy = portal['memberfolder1']['member1']
        wf.notifyCreated(dummy)
      
        wf.doActionFor(dummy, 'approve', comment='foo' )
       
        browser = Browser(app)
        browser.handleErrors = False
#        browser.addHeader('Authorization', 'Basic %s:%s' % ("12@qq.com", "391124",))
#        
#        import transaction
#        transaction.commit()
#        self.wf.doActionFor(dummy, 'approve', comment='foo' ) 
               

#        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
#        
#        import transaction
#        transaction.commit()
        # login in from login page
        browser.open(portal.absolute_url() + '/login_form')
#        browser.getControl(name='__ac_name').value = SITE_OWNER_NAME
#        browser.getControl(name='__ac_password').value = SITE_OWNER_PASSWORD        
        browser.getControl(name='__ac_name').value = "12@qq.com"
        browser.getControl(name='__ac_password').value = "391124"
        browser.getControl(name='submit').click()
        import transaction
        transaction.commit()        
        obj = portal['memberfolder1']['member1'].absolute_url() + '/view'        

        browser.open(obj)

        outstr = "I am member1"        
        self.assertTrue(outstr in browser.contents)   
        outstr = "12(at)qq.com"        
        self.assertTrue(outstr in browser.contents)
        outstr ="++add++my315ok.socialorgnization.orgnizationsurvey"
        self.assertTrue(outstr in browser.contents)          

    def test_ajax_member_state(self):
        request = self.layer['request']        
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret,TEST_USER_NAME, sha).hexdigest()
        request.form = {
                        '_authenticator': auth,
                        'state':'pending', #new created member initial status
                        'id':'member1',                                                                       
                        }
        
        view = self.portal['memberfolder1'].restrictedTraverse('@@ajaxmemberstate')
        result = view()

        self.assertEqual(json.loads(result),True)         

    def test_member_workflow(self):
        app = self.layer['app']
        portal = self.layer['portal']
        wf = getToolByName(portal, 'portal_workflow')

        wt = wf.dexterity_membrane_workflow
        dummy = portal['memberfolder1']['member1']
        wf.notifyCreated(dummy)

        chain = wf.getChainFor(dummy)
        self.failUnless(chain[0] =='dexterity_membrane_workflow')

        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'pending')        
        wf.doActionFor(dummy, 'approve', comment='foo' )

## available variants is actor,action,comments,time, and review_history        
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'enabled')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'foo')     