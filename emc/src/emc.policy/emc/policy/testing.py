#-*- coding: UTF-8 -*-
import datetime
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting,FunctionalTesting

from plone.app.testing import (
IntegrationTesting,
FunctionalTesting,
login, logout, setRoles,
PLONE_FIXTURE,
TEST_USER_NAME,
SITE_OWNER_NAME,
)

from plone.testing import z2
from plone.namedfile.file import NamedImage
from plone import namedfile
from zope.configuration import xmlconfig

def getFile(filename):
    """ return contents of the file with the given name """
    import os
    filename = os.path.join(os.path.dirname(__file__) + "/tests/", filename)
    return open(filename, 'r')

class SitePolicy(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)
    
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import plone.app.contenttypes
        import emc.policy
        import emc.theme
        import emc.project
        import emc.kb
        import emc.bokeh
        import emc.memberArea
        xmlconfig.file('configure.zcml', plone.app.contenttypes, context=configurationContext)
        xmlconfig.file('configure.zcml', emc.policy, context=configurationContext)
        xmlconfig.file('configure.zcml', emc.theme, context=configurationContext)
        xmlconfig.file('configure.zcml', emc.bokeh, context=configurationContext)
        xmlconfig.file('configure.zcml', emc.kb, context=configurationContext)
        xmlconfig.file('configure.zcml', emc.memberArea, context=configurationContext)
        xmlconfig.file('configure.zcml', emc.project, context=configurationContext)
     
        # Install products that use an old-style initialize() function

       
    
    def tearDownZope(self, app):
        # Uninstall products installed above
        pass

     
        
    def setUpPloneSite(self, portal):
        applyProfile(portal, 'emc.policy:default')
        applyProfile(portal, 'emc.theme:default')
        applyProfile(portal, 'emc.bokeh:default')
        applyProfile(portal, 'emc.kb:default')
        applyProfile(portal, 'emc.project:default')


class IntegrationSitePolicy(SitePolicy):      
        
    def setUpPloneSite(self, portal):
        applyProfile(portal, 'emc.policy:default')
        applyProfile(portal, 'emc.theme:default')
        applyProfile(portal, 'emc.bokeh:default')
        applyProfile(portal, 'emc.kb:default')
        applyProfile(portal, 'emc.project:default')
#        portal = self.layer['portal']
        #make global request work
        from zope.globalrequest import setRequest
        setRequest(portal.REQUEST)
        # login doesn't work so we need to call z2.login directly
        z2.login(portal.__parent__.acl_users, SITE_OWNER_NAME)
            
        self.portal = portal 

POLICY_FIXTURE = SitePolicy()
INTEGRATION_FIXTURE = IntegrationSitePolicy()
INTEGRATION_TESTING = IntegrationTesting(bases=(INTEGRATION_FIXTURE,), name="Site:Integration")
FunctionalTesting = FunctionalTesting(bases=(POLICY_FIXTURE,), name="Site:FunctionalTesting")