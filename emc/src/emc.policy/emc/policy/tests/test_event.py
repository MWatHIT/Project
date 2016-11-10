#-*- coding: UTF-8 -*-

from zope import event
from zope.lifecycleevent import IObjectAddedEvent, ObjectAddedEvent
from Products.CMFCore.utils import getToolByName
from xtshzz.policy.testing import POLICY_INTEGRATION_TESTING ,FunctionalTesting

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
        portal['orgnizationfolder1'].invokeFactory('my315ok.socialorgnization.governmentorgnization','government1',
                                                   title=u"商务局",
                                                   description=u"运输业",
                                                   address=u"建设北路",
                                                   register_code="834100",
                                                   supervisor=u"交通局",
                                                   operator = "tyj@qq.com",
                                                   organization_type="minfei",
                                                   legal_person=u"张建明",
                                                   passDate =datetime.datetime.today(),
                                                   belondto_area='xiangtanshi', 
                                                   )                  
        portal['orgnizationfolder1']['orgnization1'].invokeFactory('my315ok.socialorgnization.orgnizationsurvey','orgnizationsurvey1',
                                                   title=u"宝庆商会1",
                                                   description=u"运输业",
                                                   annual_survey="hege",
                                                   year="2013",

                                                   )
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
                             orgname = 'orgnization1',
                             description="I am member1")     
        
        portal['memberfolder1'].invokeFactory('dexterity.membrane.sponsormember', '568066794',
                             email="568066794@qq.com",
                             last_name=u"唐",
                             first_name=u"岳军",
                             title = u"tangyuejun",
                             password="391124",
                             confirm_password ="391124",
                             homepae = 'http://315ok.org/',
                             orgname = 'government1',
                             description="I am member1")  

        data = getFile('image.jpg').read()
        item = portal['memberfolder1']['member1']
        item.photo = NamedImage(data, 'image/jpg', u'image.jpg')        
           
        self.portal = portal
    
    def test_update_operator(self):
        item = self.portal['memberfolder1']['568066794']
        event.notify(ObjectAddedEvent(item,self.portal['memberfolder1'],'568066794'))
        sorg = self.portal['orgnizationfolder1']['government1']
        self.assertEqual(sorg.operator,"568066794@qq.com") 
        
    def test_org_adapter(self):
        from xtshzz.policy.behaviors.org import IOrg
        app = self.layer['app']
        portal = self.layer['portal']
        member = portal['memberfolder1']['member1']
        org = portal['orgnizationfolder1']['orgnization1']
        path = IOrg(member).getOrgPath()
        lp = IOrg(member).getOrgBn().orgnization_legalPerson
        sr = IOrg(member).getOrgBn().orgnization_supervisor
        self.assertEqual(lp,u"张建明") 
        self.assertEqual(sr,u"交通局") 
        self.assertEqual(path,org.absolute_url())        
