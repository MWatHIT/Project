from plone.app.testing import PloneSandboxLayer
from plone.app.testing.bbb import PTC_FIXTURE
from plone.app.testing import IntegrationTesting, FunctionalTesting

from plone.testing import z2


class Fixture(PloneSandboxLayer):

    defaultBases = (PTC_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.app.contenttypes
        import plone.dexterity
        import collective.filepreviewbehavior
#         import plone.app.versioningbehavior
#         import Products.CMFPlacefulWorkflow
        self.loadZCML(package=plone.app.contenttypes)
        self.loadZCML(package=plone.dexterity)
        self.loadZCML(package=collective.filepreviewbehavior)

#         z2.installProduct(app, 'Products.CMFPlacefulWorkflow')

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'plone.app.contenttypes:default')


FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(PTC_FIXTURE,),
    name="Integration",
)

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PTC_FIXTURE,),
    name="Functional",
)
FUNCTIONAL_TESTING2 = FunctionalTesting(
    bases=(FIXTURE,),
    name="Functional2",
)
