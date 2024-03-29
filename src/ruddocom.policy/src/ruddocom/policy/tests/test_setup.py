# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID
from ruddocom.policy.testing import RUDDOCOM_POLICY_INTEGRATION_TESTING  # noqa: E501

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that ruddocom.policy is properly installed."""

    layer = RUDDOCOM_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if ruddocom.policy is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'ruddocom.policy'))

    def test_browserlayer(self):
        """Test that IRuddocomPolicyLayer is registered."""
        from ruddocom.policy.interfaces import (
            IRuddocomPolicyLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IRuddocomPolicyLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = RUDDOCOM_POLICY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['ruddocom.policy'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if ruddocom.policy is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'ruddocom.policy'))

    def test_browserlayer_removed(self):
        """Test that IRuddocomPolicyLayer is removed."""
        from ruddocom.policy.interfaces import \
            IRuddocomPolicyLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IRuddocomPolicyLayer,
            utils.registered_layers())
