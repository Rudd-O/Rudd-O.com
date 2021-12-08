#!/usr/bin/env python

import contextlib
import logging
import os
import sys
from pathlib import Path
from io import BytesIO

import transaction
from zope.component.hooks import setSite
from zope.i18n import translate
from plone import api
from Acquisition import aq_get
from Testing.makerequest import makerequest
from Products.CMFCore.tests.base.security import (
    PermissiveSecurityPolicy,
    OmnipotentUser,
)
from AccessControl.SecurityManager import setSecurityPolicy
from AccessControl.SecurityManagement import newSecurityManager
from operator import itemgetter



logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.INFO)


def portal_types(request):
    """A list with info on all content types with existing items."""
    catalog = api.portal.get_tool("portal_catalog")
    portal_types = api.portal.get_tool("portal_types")
    results = []
    for fti in portal_types.listTypeInfo():
        query = {}
        query["portal_type"] = fti.id
        number = len(catalog.unrestrictedSearchResults(**query))
        if number >= 1:
            results.append(
                {
                    "number": number,
                    "value": fti.id,
                    "title": translate(
                        fti.title, domain="plone", context=request
                    ),
                }
            )
    return sorted(results, key=itemgetter("title"))


def full_export(portal, from_path, outputpath, what=''):
    if not from_path.startswith("/"):
        from_path = "/" + from_path
    request = aq_get(portal, "REQUEST")

    # Workaround to enable import view, otherwise it fails.
    request.form["form.submitted"] = True

    for step in 'content relations translations members localroles defaultpages ordering discussion portlets'.split():
        if what and step not in what:
            continue
        if step == "content":
            logger.error("Skipping %s since it does not work", step)
            continue
        logger.info("Exporting %s from site", step)
        export_view = api.content.get_view("export_%s" % step, portal, request)
        if step == "content":
            types = [x['value'] for x in portal_types(request)]
            export_view(portal_type=types, download_to_server=1, migration=True, path=from_path, include_blobs=2)
        else:
            request.response.stdout = BytesIO()
            request.response._wrote = 0
            export_view()
            request.response.stdout.seek(0, 0)
            reply = request.response.stdout.read()
            pos = reply.find(b"\r\n\r\n")
            assert pos > 0, reply[:100]
            data = reply[pos+4:]
            with open(os.path.join(outputpath, "%s.json" % step), "wb") as f:
                f.write(data)

    del request.form["form.submitted"]

    step = "redirects"
    if not what or step in what:
        # Workaround to enable CSV download.
        request.form["form.button.Download"] = "Download+all+as+CSV"
        logger.info("Exporting %s from site", step)
        view = api.content.get_view("redirection-controlpanel", portal, request)
        with view() as fobj:
            data = fobj.read()
            with open(os.path.join(outputpath, "%s.json" % step), "wb") as f:
                f.write(data)

    logger.info("Done exporting site")

args = sys.argv[3:]

if not args:
    raise Exception("the site to export should be the first argument")
if len(args) < 2:
    raise Exception("the path to export the data to should be the second argument")

siteid = args[0]
exportpath = args[0]
outputpath = args[1]
what = args[2] if len(args) > 2 else ''

site = app.unrestrictedTraverse(siteid)
site = makerequest(site)
setSite(site)

full_export(site, exportpath, outputpath, what=what)
