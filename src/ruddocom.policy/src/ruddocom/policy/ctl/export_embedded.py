#!/usr/bin/env python

import contextlib
from io import BytesIO
import logging
from operator import itemgetter
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
from zope.component.hooks import setSite
from zope.globalrequest import setRequest
from zope.i18n import translate


logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.INFO)
logging.getLogger("collective.exportimport").setLevel(logging.INFO)


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


@contextlib.contextmanager
def wrapped_request(request):
    old = (request.response.stdout, request.response._wrote)
    stdout = BytesIO()
    request.response.stdout = stdout
    request.response._wrote = 0
    def f():
        stdout.seek(0, 0)
        reply = stdout.read()
        pos = reply.find(b"\r\n\r\n")
        assert pos > 0, reply[:100]
        data = reply[pos+4:]
        return data
    try:
        yield f
    finally:
        request.response.stdout, request.response._wrote = old


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
        with wrapped_request(request) as reader:
            if step == "content":
                types = [x['value'] for x in portal_types(request)]
                export_view(portal_type=types, download_to_server=0, migration=True, path=from_path, include_blobs=2)
            else:
                export_view()
        data = reader()
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
            with open(os.path.join(outputpath, "%s.csv" % step), "wb") as f:
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
site_with_request = makerequest(site)
site_with_request.REQUEST["PARENTS"] = [site, app]
setRequest(site_with_request.REQUEST)
setSite(site_with_request)

full_export(site_with_request, exportpath, outputpath, what=what)
