# -*- coding: utf-8 -*-
import logging

from plone import api
from Acquisition import aq_inner
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from zope.component import getUtility
from plone.app.multilingual.browser.setup import SetupMultilingualSite
from plone.app.redirector.interfaces import IRedirectionStorage
from zope.component import getUtility, getMultiAdapter
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import (
    IPortletAssignmentMapping,
    IPortletAssignmentSettings,
)


PROFILE = "manuelamador.policy:default"
logger = logging.getLogger(__name__).warning


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "manuelamador.policy:uninstall",
        ]


def post_install(context):
    """Post install script"""
    hide_colophon_and_footer(context)
    setup_cookies(context)
    logger("Post-install complete")


def setup_cookies(context):
    portal_url = api.portal.get_tool("portal_url")
    portal = portal_url.getPortalObject()
    l = portal.acl_users.session
    changed = False
    t = 30 * 24 * 86400
    if l.timeout != t:
        # Session times out in 30 days.
        l.timeout = t
        changed = True
    f = 0
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


def hide_colophon_and_footer(context=None):
    portal = api.portal.get()
    manager_name = "plone.footerportlets"
    changed = False
    mapping = get_portlet_assignments(manager_name, portal)
    for id_, assignment in mapping.items():
        if id_ != "colophon" and id != "footer":
            continue
        assignments = aq_inner(portal)
        settings = IPortletAssignmentSettings(assignment)
        if settings.get("visible", "unset") in (True, "unset"):
            changed = True
            settings["visible"] = False
    if changed:
        logger("Successfully hid the colophon and default footer")
