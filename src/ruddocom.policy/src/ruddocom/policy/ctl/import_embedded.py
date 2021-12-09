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


def remove_lrfs():
    catalog = api.portal.get_tool('portal_catalog')
    results = catalog.searchResults(**{'portal_type': 'LRF'})

    deleted = False
    for r in results:
        obj = r.getObject()
        parent = obj.aq_parent
        logger.info("Deleting %s from %s", obj.id, parent.id)
        del parent[obj.id]
        deleted = True
    if deleted:
        logger.info("Recataloguing everything")
        catalog.clearFindAndRebuild()


class fakeredirectsfile(object):
    def __init__(self, fobject):
        self.filename = fobject.name
        self.data = fobject.readlines()
        if self.data and self.data[0].strip().endswith("datetime,manual"):
            self.data = self.data[1:]
        self.data = "".join(self.data)

    def read(self):
        return self.data


class StatusObject(object):

    def __init__(self):
        self.messages = []

    def addStatusMessage(self, *a, **kw):
        self.messages.append((a, kw))


def full_import(portal, from_path, what=''):
    from_path = Path(from_path)
    request = aq_get(portal, "REQUEST")

    # Workaround to enable import view, otherwise it fails.
    request.form["form.submitted"] = True

    for step in 'content translations relations members ordering defaultpages localroles discussion portlets'.split():
        if what and step not in what:
            continue

        if step == "content":
            remove_lrfs()

        logger.info("Importing %s to site", step)
        import_view = api.content.get_view("import_%s" % step, portal, request)
        path = from_path / ("%s.json" % step)
        import_view(jsonfile=path.read_text(), return_json=True)

    del request.form["form.submitted"]

    step = "redirects"
    if step in what or not what:
        # Workaround to enable CSV download.
        request.form["form.button.Upload"] = "Download+all+as+CSV"
        path = from_path / ("%s.csv" % step)
        with path.open("r") as fo:
            f = fakeredirectsfile(fo)
        request.form["file"] = f
        logger.info("Importing %s to site", step)
        view = api.content.get_view("redirection-controlpanel", portal, request)
        view.csv_errors = []
        view.form_errors = {}
        statusObject = StatusObject()
        view.upload(f, portal, getUtility(IRedirectionStorage), statusObject)
        if view.form_errors:
            assert 0, view.form_errors
        if view.csv_errors:
            assert 0, "Errors during redirects import:\n\n" + "\n".join(str(s) for s in view.csv_errors)
    del request.form["form.button.Upload"]
    del request.form["file"]

    request.form["form.submitted"] = True

    if "fix_html" in what or not what:
        logger.info("Fixing HTML on imported content")
        fixer = api.content.get_view("fix_html", portal, request)
        fixer()

    if "fix_collection_queries" in what or not what:
        logger.info("Fixing collection queries")
        fixer = api.content.get_view("fix_collection_queries", portal, request)
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
