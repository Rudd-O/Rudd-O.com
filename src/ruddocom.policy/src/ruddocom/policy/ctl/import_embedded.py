#!/usr/bin/env python

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


@contextlib.contextmanager
def externalEditorEnabled(app):
    # Workaround to bypass the externalEditorEnabled demand
    app.externalEditorEnabled = False
    try:
        yield
    finally:
        delattr(app, "externalEditorEnabled")


def full_import(portal, from_path):
    from_path = Path(from_path)
    request = aq_get(portal, "REQUEST")

    # Workaround to enable import view, otherwise it fails.
    request.form["form.submitted"] = True

    import_content = api.content.get_view("import_content", portal, request)
    path = from_path / "content.json"
    import_content(jsonfile=path.read_text(), return_json=True)
    return

    import_translations = api.content.get_view("import_translations", portal, request)
    path = from_path / "translations.json"
    import_translations(jsonfile=path.read_text())

    import_relations = api.content.get_view("import_relations", portal, request)
    path = from_path / "relations.json"
    import_relations(jsonfile=path.read_text())

    import_members = api.content.get_view("import_members", portal, request)
    path = from_path / "members.json"
    import_members(jsonfile=path.read_text())

    import_ordering = api.content.get_view("import_ordering", portal, request)
    path = from_path / "ordering.json"
    import_ordering(jsonfile=path.read_text())

    import_defaultpages = api.content.get_view("import_defaultpages", portal, request)
    path = from_path / "defaultpages.json"
    import_defaultpages(jsonfile=path.read_text())

    reset_modified = api.content.get_view("reset_modified_date", portal, request)
    reset_modified()


args = sys.argv[3:]

commit = True
if "-n" in args:
    commit = False
    args.remove("-n")

if not args:
    raise Exception("the site to import should be the first argument")

siteid = args[0]
importpath = args[1]

site = app.unrestrictedTraverse(siteid)
site = makerequest(site)
setSite(site)

with externalEditorEnabled(app):
    full_import(site, importpath)

if commit:
    t = transaction.get()
    t.note("Import on %s completed" % siteid)
    t.commit()
