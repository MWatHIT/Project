#-*- coding: UTF-8 -*-
from Products.CMFCore.utils import getToolByName
from emc.policy.testing import INTEGRATION_TESTING,FunctionalTesting 

from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles,logout
from plone.testing.z2 import Browser
import unittest2 as unittest
from plone.namedfile.file import NamedImage
import os
from dexterity.membrane.membrane_helpers import get_user_id_for_email

from Products.CMFCore.utils import getToolByName

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
# create member 
       
        portal.invokeFactory('dexterity.membrane.memberfolder', 'memberfolder1')        
        portal['memberfolder1'].invokeFactory('dexterity.membrane.organizationmember', 'member1',
                             email="12@qq.com",
                             last_name=u"唐",
                             first_name=u"岳军",
                             title = u"tangyuejun",
                             password="391124",
                             confirm_password ="391124",
                             homepae = 'http://315ok.org/',
                             bonus = 10,
                             description="I am member1")     

        portal['memberfolder1'].invokeFactory('dexterity.membrane.organizationmember', 'member2',
                             email="13@qq.com",
                             last_name=u"唐",
                             first_name=u"岳军",
                             title = u"tangyuejun",
                             password="391124",
                             confirm_password ="391124",
                             homepae = 'http://315ok.org/',
                             bonus = 300,
                             description="I am member1") 
        data = getFile('image.jpg').read()
        item = portal['memberfolder1']['member1']
        item.photo = NamedImage(data, 'image/jpg', u'image.jpg')
# create organization object
        portal.invokeFactory('my315ok.socialorgnization.orgnizationfolder', 'orgnizationfolder1',
                             title="orgnizationfolder1",description="demo orgnizationfolder")
        portal['orgnizationfolder1'].invokeFactory('my315ok.socialorgnization.orgnization','orgnization1',
                                                   title=u"宝庆商会",
                                                   description=u"运输业",
                                                   address=u"建设北路",
                                                   register_code="8341",
                                                   supervisor=u"交通局",
                                                   organization_type="minfei",
                                                   legal_person=u"张建明",
                                                   passDate =datetime.datetime.today(),
                                                   belondto_area='yuhuqu', 
                                                   )
        
        portal['orgnizationfolder1'].invokeFactory('my315ok.socialorgnization.orgnization','orgnization2',
                                                   title=u"宝庆商会",
                                                   description=u"运输业",
                                                   address=u"建设北路",
                                                   register_code="834100",
                                                   supervisor=u"交通局",
                                                   organization_type="minfei",
                                                   legal_person=u"张建明",
                                                   passDate =datetime.datetime.today(),
                                                   belondto_area='xiangtanshi', 
                                                   ) 
               
        portal['orgnizationfolder1'].invokeFactory('my315ok.socialorgnization.orgnization','orgnization3',
                                                   title=u"宝庆商会",
                                                   description=u"运输业",
                                                   address=u"建设北路",
                                                   register_code="834100",
                                                   supervisor=u"交通局",
                                                   organization_type="minfei",
                                                   legal_person=u"张建明",
                                                   passDate =datetime.datetime.today(),
                                                   belondto_area='xiangtanshi', 
                                                   ) 
               

        data = getFile('image.gif').read()
        item = portal['orgnizationfolder1']['orgnization1']
        item.image = NamedImage(data, 'image/gif', u'image.gif')
        data2 = getFile('image.jpg').read()        
        item2 = portal['orgnizationfolder1']['orgnization2']
        item2.image = NamedImage(data2, 'image/jpeg', u'image.jpg')  
        data3 = getFile('image.png').read()        
        item3 = portal['orgnizationfolder1']['orgnization3']
        item3.image = NamedImage(data3, 'image/png', u'image.png')
         
        portal['orgnizationfolder1']['orgnization1'].invokeFactory('my315ok.socialorgnization.orgnizationsurvey','orgnizationsurvey1',
                                                   title=u"宝庆商会1",
                                                   description=u"运输业",
                                                   annual_survey="hege",
                                                   year="2013",

                                                   )                                  
        
           
        self.portal = portal
    
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

    def test_survey_workflow(self):
        app = self.layer['app']
        portal = self.layer['portal']
        wf = getToolByName(portal, 'portal_workflow')

        wt = wf.organization_anual_survey_workflow
        org = portal['orgnizationfolder1']['orgnization1']        
        dummy = org['orgnizationsurvey1']
        wf.notifyCreated(dummy)

        chain = wf.getChainFor(dummy)
        self.failUnless(chain[0] =='organization_anual_survey_workflow')

        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'draft')        
        wf.doActionFor(dummy, 'submit2sponsor', comment='submit to sponsor' )

## available variants is actor,action,comments,time, and review_history        
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'pendingsponsor')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'submit to sponsor')         

# sponsor agree
        wf.doActionFor(dummy, 'sponsoragree', comment='sponsor has been agree' )       
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'pendingagent')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'sponsor has been agree')  

# agent agree
        wf.doActionFor(dummy, 'agentagree', comment='agent has been agree' )       
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'published')

# agent retract
        wf.doActionFor(dummy, 'retract', comment='agent has been retract' )       
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'draft')
# direct submit to agent        
        wf.doActionFor(dummy, 'submit2agent', comment='submit to agent' )       
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'pendingagent') 

# agent reject to owner       
        wf.doActionFor(dummy, 'agentreject', comment='agent reject to owner' )       
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'draft')

# sponsor reject to owner       
        wf.doActionFor(dummy, 'submit2sponsor', comment='submit to sponsor again' )       
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'pendingsponsor')
    
        wf.doActionFor(dummy, 'sponsorreject', comment='sponsor reject to owner' )       
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'draft')        
                              
    def test_permission_workflow(self):
        app = self.layer['app']
        portal = self.layer['portal']
        wf = getToolByName(portal, 'portal_workflow')


        org = portal['orgnizationfolder1']['orgnization1']
        
        wts = wf.organization_anual_survey_workflow
        survey = org['orgnizationsurvey1']
        wts.notifyCreated(survey)     
               

        wt = wf.dexterity_membrane_workflow
        dummy = portal['memberfolder1']['member1']
        wf.notifyCreated(dummy)
        dummy.email = 'JOE@example.org'
        dummy.password = 'secret'
        dummy.confirm_password = 'secret'
        membrane = getToolByName(portal, 'membrane_tool')
        membrane.reindexObject(dummy)

        # Uppercase:
        user_id = get_user_id_for_email(portal,'JOE@example.org')                
        aclu = getToolByName(portal, 'acl_users')
        auth = aclu.membrane_users.authenticateCredentials
        credentials = {'login': 'JOE@example.org', 'password': 'secret'}
        # First the member needs to be enabled before authentication
        # can succeed.
        self.assertEqual(auth(credentials), None)
        wf_tool = getToolByName(self.layer['portal'], 'portal_workflow')
        login(self.layer['portal'], TEST_USER_NAME)
        setRoles(self.layer['portal'], TEST_USER_ID, ['Reviewer'])
        wf_tool.doActionFor(dummy, 'approve')
        logout()

        self.assertEqual(auth(credentials), (user_id, 'JOE@example.org'))        

        memship = getToolByName(portal, 'portal_membership')
        joe_member = memship.getMemberById(user_id)
        self.assertTrue(joe_member)

        # At first, no one gets an extra local role, because the
        # members are not enabled.
        # Test roles of fresh joe:

        self.assertEqual(
            joe_member.getRolesInContext(self.layer['portal']),
            ['Social Organization', 'Authenticated']
        )

        self.assertEqual(sorted(joe_member.getRolesInContext(dummy)),
        ['Authenticated', u'Creator', u'Editor', u'Reader', 'Social Organization'])


     
      
        
   