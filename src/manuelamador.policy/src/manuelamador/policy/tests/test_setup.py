# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID
from manuelamador.policy.testing import MANUELAMADOR_POLICY_INTEGRATION_TESTING  # noqa: E501

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that manuelamador.policy is properly installed."""

    layer = MANUELAMADOR_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if manuelamador.policy is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'manuelamador.policy'))

    def test_browserlayer(self):
        """Test that IManuelAmadorPolicyLayer is registered."""
        from manuelamador.policy.interfaces import (
            IManuelAmadorPolicyLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IManuelAmadorPolicyLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = MANUELAMADOR_POLICY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['manuelamador.policy'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if manuelamador.policy is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'manuelamador.policy'))

    def test_browserlayer_removed(self):
        """Test that IManuelAmadorPolicyLayer is removed."""
        from manuelamador.policy.interfaces import \
            IManuelAmadorPolicyLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IManuelAmadorPolicyLayer,
            utils.registered_layers())
