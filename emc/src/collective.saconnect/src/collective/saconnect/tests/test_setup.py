# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.saconnect.testing import COLLECTIVE_SACONNECT_INTEGRATION_TESTING  # noqa
from Products.CMFCore.utils import getToolByName

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.saconnect is properly installed."""

    layer = COLLECTIVE_SACONNECT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = getToolByName(self.portal, 'portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.saconnect is installed with
           portal_quickinstaller.
        """
        self.assertTrue(
            self.installer.isProductInstalled(
                'collective.saconnect'
            )
        )

    def test_uninstall(self):
        """Test if collective.saconnect is cleanly uninstalled."""
        self.installer.uninstallProducts(['collective.saconnect'])
        self.assertFalse(
            self.installer.isProductInstalled(
                'collective.saconnect'
            )
        )
        # self.assertNotIn('authomatic', self.portal.acl_users)

    def test_browserlayer(self):
        """Test that IPasPluginsAuthomaticLayer is registered."""
        from collective.saconnect.interfaces import ICollectiveSAConnectLayer  # noqa
        from plone.browserlayer import utils
        self.assertTrue(
            ICollectiveSAConnectLayer in utils.registered_layers()
        )
