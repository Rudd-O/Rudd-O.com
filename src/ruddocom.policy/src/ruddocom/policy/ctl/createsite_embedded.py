#!/usr/bin/env python

# https://github.com/plone/ansible.plone_server/blob/master/templates/addPloneSite.py.j2

import sys
import transaction

from Products.CMFPlone.factory import _DEFAULT_PROFILE
from Products.CMFPlone.factory import addPloneSite


args = sys.argv[3:]
commit = True
if "-n" in args:
    commit = False
    args.remove("-n")
site_id = args[0]
site_title = args[1] if len(args) > 1 else ""
profiles = [
    "plonetheme.barceloneta:default",
    "plone.app.contenttypes:default",
    "plone.app.caching:default",
] + args[2:]

addPloneSite(
    app,
    site_id,
    title=site_title,
    profile_id=_DEFAULT_PROFILE,
    setup_content=False,
    extension_ids=profiles,
)

if commit:
    t = transaction.get()
    t.note("Created Plone site %s" % site_id)
    t.commit()
