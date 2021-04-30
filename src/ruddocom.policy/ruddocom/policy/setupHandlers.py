# -*- coding: utf-8 -*-

import logging

from Products.CMFCore.utils import getToolByName


default_profile = "profile-ruddocom.policy:default"
logger = logging.getLogger("ruddocom.policy")
logger = logger.warning


def setupCookies(portal_setup):
    logger("Setting cookie expiry time.")
    portal_url = getToolByName(portal_setup, "portal_url")
    portal = portal_url.getPortalObject()
    l = portal.acl_users.session
    l.timeout = 604800
    l.cookie_lifetime = 30
    l.secure = True
    logger("Cookie expiry time set.")


def setupRegistryProperties(portal_setup):
    logger("Setting up registry properties.")
    portal_setup.runImportStepFromProfile(
        "ruddocom.policy:default", "plone.app.registry"
    )
    logger("Done setting up registry properties.")


def setupAll(portal_setup):
    try:
        if portal_setup.readDataFile("ruddocom.policy.txt") is None:
            return
    except AttributeError:
        logger("Called with %s, continuing since it appears we do not need a marker file.", portal_setup)
    logger("Beginning setupAll with context %s.", portal_setup)
    setupCookies(portal_setup)
    setupRegistryProperties(portal_setup)
    logger("Ended setupAll with context %s.", portal_setup)
