# -*- coding: utf-8 -*-
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer

import collective.saconnect


class CollectiveSAConnectLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.saconnect)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.saconnect:default')


COLLECTIVE_SACONNECT_FIXTURE = CollectiveSAConnectLayer()


COLLECTIVE_SACONNECT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_SACONNECT_FIXTURE,),
    name='CollectiveSAConnectLayer:IntegrationTesting'
)


COLLECTIVE_SACONNECT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_SACONNECT_FIXTURE,),
    name='CollectiveSAConnectLayer:FunctionalTesting'
)
