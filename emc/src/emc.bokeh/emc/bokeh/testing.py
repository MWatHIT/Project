import os
import tempfile



from plone.app.contenttypes.tests.robot.variables import TEST_FOLDER_ID
# from plone.app.event.testing import PAEvent_FIXTURE
# from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import TEST_USER_ID
from plone.app.testing import applyProfile
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.testing import z2
from zope.configuration import xmlconfig
from zope.interface import alsoProvides
import pkg_resources

from zope.configuration import xmlconfig

class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)
    
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import emc.bokeh
        xmlconfig.file('configure.zcml', emc.bokeh, context=configurationContext)        
        import emc.policy
        xmlconfig.file('configure.zcml', emc.policy, context=configurationContext)
                      
    def tearDownZope(self, app):
        pass
    
    def setUpPloneSite(self, portal):
     
        applyProfile(portal, 'emc.bokeh:test')
#        applyProfile(portal, 'xtshzz.policy:default')
     

FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(bases=(FIXTURE,), name="emcbokeh:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(bases=(FIXTURE,), name="emcbokeh:Functional")

# from plone.app.contenttypes.testing import PloneAppContenttypes
class codeFileContenttypes(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import emc.bokeh  
        xmlconfig.file('configure.zcml', emc.bokeh, context=configurationContext)        
        import emc.policy
        xmlconfig.file('configure.zcml', emc.policy, context=configurationContext)

        import plone.app.contenttypes
        xmlconfig.file(
            'configure.zcml',
            plone.app.contenttypes,
            context=configurationContext
        )

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plone.app.contenttypes:default')
        applyProfile(portal, 'emc.bokeh:test')

        mtr = portal.mimetypes_registry
        mime_doc = mtr.lookup('application/msword')[0]
        mime_doc.icon_path = 'custom.png'

        portal.acl_users.userFolderAddUser('admin',
                                           'secret',
                                           ['Manager'],
                                           [])
        login(portal, 'admin')
        portal.portal_workflow.setDefaultChain("simple_publication_workflow")
        setRoles(portal, TEST_USER_ID, ['Manager'])
        portal.invokeFactory(
            "Folder",
            id=TEST_FOLDER_ID,
            title=u"Test Folder"
        )

    def tearDownPloneSite(self, portal):
        applyProfile(portal, 'plone.app.contenttypes:uninstall')
        
PLONE_APP_CONTENTTYPES_FIXTURE = codeFileContenttypes()
PLONE_APP_CONTENTTYPES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONE_APP_CONTENTTYPES_FIXTURE,),
    name="codeFileContenttypes:Integration"
)
PLONE_APP_CONTENTTYPES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONE_APP_CONTENTTYPES_FIXTURE,),
    name="codeFileContenttypes:Functional"
)


