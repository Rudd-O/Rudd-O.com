# -*- coding: utf-8 -*-
import logging

from Acquisition import aq_inner
from Products.CMFPlone.interfaces import INonInstallable
from plone import api
from plone.app.multilingual.browser.setup import SetupMultilingualSite
from plone.app.redirector.interfaces import IRedirectionStorage
from plone.portlets.interfaces import (
    IPortletAssignmentMapping,
    IPortletAssignmentSettings,
)
from plone.portlets.interfaces import IPortletManager
from zope.component import getUtility, getMultiAdapter
from zope.interface import implementer


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
    setup_folderish_types(context)
    hide_colophon(context)
    destroy_portlets_in_lrfs(context)
    setup_cookies(context)
    logger("Post-install complete")


def setup_cookies(unused_context):
    portal_url = api.portal.get_tool("portal_url")
    portal = portal_url.getPortalObject()
    l = portal.acl_users.session
    changed = False
    t = 30 * 24 * 86400
    if l.timeout != t:
        # Session times out in 30 days.
        l.timeout = t
        changed = True
    f = 30
    if l.cookie_lifetime != f:
        # Cookie lasts forever.
        l.cookie_lifetime = f
        changed = True
    if not l.secure:
        # Cookie is network-only.
        l.secure = True
        changed = True
    if changed:
        logger("Cookie expiry time, lifetime, and security status set.")


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def get_portlet_assignments(manager_name, for_):
    manager = getUtility(IPortletManager, name=manager_name, context=for_)
    mapping = getMultiAdapter((for_, manager), IPortletAssignmentMapping)
    return mapping


def hide_colophon(context=None):
    portal = api.portal.get()
    manager_name = "plone.footerportlets"
    changed = False
    mapping = get_portlet_assignments(manager_name, portal)
    for id_, assignment in mapping.items():
        if id_ != "colophon":
            continue
        assignments = aq_inner(portal)
        settings = IPortletAssignmentSettings(assignment)
        if settings.get("visible", "unset") in (True, "unset"):
            changed = True
            settings["visible"] = False
    if changed:
        logger("Successfully hid the colophon")


def destroy_portlets_in_lrfs(context=None):
    portal = api.portal.get()
    manager_name = "plone.footerportlets"
    for folder_id in ["en", "es"]:
        mapping = get_portlet_assignments(manager_name, portal[folder_id])
        changed = False
        for id_, unused_assignment in list(mapping.items()):
            changed = True
            del mapping[id_]
    if changed:
        logger("Successfully destroyed the crufty portlets")


def setup_multilingual(context=None):
    language_tool = api.portal.get_tool("portal_languages")
    language_tool.addSupportedLanguage("es")
    language_tool.addSupportedLanguage("en-us")
    setuptool = SetupMultilingualSite()
    portal = api.portal.get()
    setuptool.setupSite(portal)
    logger("Done setting up multilingual")


def add_redirect(source_path, target_path):
    storage = getUtility(IRedirectionStorage)
    storage.add(source_path, target_path)


def setup_language_folder_redirects(context=None):
    for path, redirect in [
        ("/en/assets", "/en/uploads"),
        ("/es/recursos", "/es/uploads"),
    ]:
        obj = api.content.get(path)
        phys_path = obj.absolute_url_path()
        root = phys_path[: -len(path)]
        phys_redirect = root + redirect
        add_redirect(phys_redirect, phys_path)
    logger("Done setting up language redirects")


def setup_folderish_types(context=None):
    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runAllImportStepsFromProfile(
        "profile-collective.folderishtypes.dx:default"
    )
    logger("Done importing folderish types")


def install_searchandreplace(context=None):
    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runAllImportStepsFromProfile(
        "profile-collective.searchandreplace:default"
    )
    logger("Done installing collective.searchandreplace")
