#!/usr/bin/env python

import contextlib
import logging
import os
from pathlib import Path
import sys

from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManager import setSecurityPolicy
from Acquisition import aq_get
from Products.CMFCore.tests.base.security import (
    PermissiveSecurityPolicy,
    OmnipotentUser,
)
from Testing.makerequest import makerequest
from plone import api
from plone.app.redirector.interfaces import IRedirectionStorage
import transaction
from zope.component import getUtility
from zope.component.hooks import setSite

from ruddocom.policy.setuphandlers import add_redirect


logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.INFO)


def add_redirs(portal):
    base = portal.absolute_url_path()
    en = portal["en"]
    assets = en["assets"]
    brains = api.content.find(assets)
    for brain in brains:
        objpath = brain.getPath()
        objpath = objpath[len(base):]
        enuploadspath = "/en/uploads" + objpath[len("/en/assets"):]
        esuploadspath = "/es/uploads" + objpath[len("/en/assets"):]
        uploadspath = "/uploads" + objpath[len("/en/assets"):]
        objpath = base + objpath
        for src in (enuploadspath, esuploadspath, uploadspath):
            src = base + src
            logger.info("Adding redirect %s -> %s", src, objpath)
            add_redirect(src, objpath)


args = sys.argv[3:]
commit = True
if "-n" in args:
    commit = False
    args.remove("-n")

if not args:
    raise Exception("the site to import should be the first argument")

siteid = args[0]

site = app.unrestrictedTraverse(siteid)
site = makerequest(site)
setSite(site)

t = transaction.begin()
t.note("Add redirections of on %s completed" % (siteid,))

add_redirs(site)
if commit:
    t.commit()
