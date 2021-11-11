# -*- coding: utf-8 -*-
import logging

from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from zope.component import getUtility
from plone.app.multilingual.browser.setup import SetupMultilingualSite
from plone.app.redirector.interfaces import IRedirectionStorage


PROFILE = "ruddocom.policy:default"
logger = logging.getLogger(__name__).warning


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "ruddocom.policy:uninstall",
        ]


def post_install(context):
    """Post install script"""
    setup_multilingual(context)
    setup_language_folder_redirects(context)


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
    logger("Done setting up multilingual")


def setup_language_folder_redirects(context=None):
    portal = api.portal.get()
    storage = getUtility(IRedirectionStorage)
    for path, redirect in [
        ("/en/assets", "/en/uploads"),
        ("/es/recursos", "/es/uploads"),
    ]:
        obj = api.content.get(path)
        phys_path = obj.absolute_url_path()
        root = phys_path[:-len(path)]
        phys_redirect = root + redirect
        storage.add(phys_redirect, phys_path)
    logger("Done setting up language redirects")
