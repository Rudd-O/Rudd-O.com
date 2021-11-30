#!/usr/bin/env python

import contextlib
import logging
import os
import sys
from pathlib import Path

import transaction
from zope.component.hooks import setSite
from plone import api
from Acquisition import aq_get
from Testing.makerequest import makerequest
from Products.CMFCore.tests.base.security import (
    PermissiveSecurityPolicy,
    OmnipotentUser,
)
from AccessControl.SecurityManager import setSecurityPolicy
from AccessControl.SecurityManagement import newSecurityManager



logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.INFO)



@contextlib.contextmanager
def externalEditorEnabled(app):
    # Workaround to bypass the externalEditorEnabled demand
    app.externalEditorEnabled = False
    try:
        yield
    finally:
        delattr(app, "externalEditorEnabled")


def full_import(portal, from_path, what=''):
    from_path = Path(from_path)
    request = aq_get(portal, "REQUEST")

    # Workaround to enable import view, otherwise it fails.
    request.form["form.submitted"] = True

    for step in 'content relations translations members localroles defaultpages ordering discussions portlets'.split():
        if what and step not in what:
            continue
        logger.info("Importing %s to site", step)
        import_view = api.content.get_view("import_%s" % step, portal, request)
        path = from_path / ("%s.json" % step)
        import_view(jsonfile=path.read_text(), return_json=True)

    if "fix_html" in what or not what:
        logger.info("Fixing HTML on imported content")
        fixer = api.content.get_view("fix_html" % step, portal, request)
        fixer()

    if "fix_collection_queries" in what or not what:
        logger.info("Fixing collection queries")
        fixer = api.content.get_view("fix_collection_queries" % step, portal, request)
        fixer()

    if "reset_dates" in what or not what:
        logger.info("Resetting dates on imported content")
        fixer = api.content.get_view("reset_dates", portal, request)
        fixer()


args = sys.argv[3:]

if not args:
    raise Exception("the site to import should be the first argument")

siteid = args[0]
importpath = args[1]
what = " ".join(args[2:])

site = app.unrestrictedTraverse(siteid)
site = makerequest(site)
setSite(site)

t = transaction.begin()
t.note("Import of %s on %s completed" % (what, siteid))

with externalEditorEnabled(app):
    full_import(site, importpath, what)

t.commit()
