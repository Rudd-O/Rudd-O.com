# -*- coding: utf-8 -*-
import logging

from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from plone.app.multilingual.browser.setup import SetupMultilingualSite


PROFILE = "ruddocom.policy:default"
logger = logging.getLogger(PROFILE.split(":")[0]).warning


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "ruddocom.policy:uninstall",
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def setup_multilingual(context=None):
    language_tool = api.portal.get_tool("portal_languages")
    language_tool.addSupportedLanguage("es")
    language_tool.addSupportedLanguage("en-us")
    setuptool = SetupMultilingualSite()
    portal = api.portal.get()
    setuptool.setupSite(portal)
