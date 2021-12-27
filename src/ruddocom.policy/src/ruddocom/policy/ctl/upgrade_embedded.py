#!/usr/bin/env python

import sys

from Products.CMFPlone.utils import get_installer
import transaction
from zope.component.hooks import setSite


productstoupgrade = sys.argv[3:]

commit = True
force = False
if "-n" in productstoupgrade:
    commit = False
    productstoupgrade.remove("-n")
if "-f" in productstoupgrade:
    force = True
    productstoupgrade.remove("-f")

if not productstoupgrade:
    raise Exception(
        "the product(s) to upgrade must " "be specified after the upgrade subcommand"
    )

if len(productstoupgrade) < 2:
    raise Exception("the product(s) to upgrade must follow the name (ID) of the site")

siteid = productstoupgrade[0]
productstoupgrade = productstoupgrade[1:]

changes = []

site = app[siteid]  # pylint:disable=invalid-name,used-before-assignment
setSite(site)

qi = get_installer(site)

t = transaction.get()
t.note("Products upgraded on %s: %s" % (siteid, ", ".join(productstoupgrade)))

for productid in productstoupgrade:
    if force:
        prof = qi.get_install_profile(productid)
        if not prof:
            raise Exception("Could not reinstall %s: no profile found." % prof)
        profid = prof["id"]
        qi.ps.runAllImportStepsFromProfile('profile-%s' % profid)
        changes.append("Product %s forcefully reinstalled on %s." % (productid, siteid))
    elif not qi.is_product_installed(productid):
        if not qi.install_product(productid):
            raise Exception("Product %s not installed." % productid)
        changes.append("Product %s successfully installed on %s." % (productid, siteid))
    else:
        if not qi.upgrade_product(productid):
            raise Exception("Product %s not upgraded." % productid)
        changes.append("Product %s successfully upgraded on %s." % (productid, siteid))

if commit:
    t.commit()
for change in changes:
    print(change + (" (Simulated.)" if not commit else ""))
