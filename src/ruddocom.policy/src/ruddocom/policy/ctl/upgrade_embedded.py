#!/usr/bin/env python

import sys

from Products.CMFPlone.utils import get_installer
import transaction
from zope.component.hooks import setSite


productstoupgrade = sys.argv[3:]

commit = True
if "-n" in productstoupgrade:
    commit = False
    productstoupgrade.remove("-n")

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

for productid in productstoupgrade:
    if qi.is_product_installed(productid):
        qi.upgrade_product(productid)
        changes.append("Product %s successfully upgraded on %s." % (productid, siteid))
    else:
        qi.install_product(productid)
        changes.append("Product %s successfully installed on %s." % (productid, siteid))

if commit:
    t = transaction.get()
    t.note("Products upgraded on %s: %s" % (siteid, ", ".join(productstoupgrade)))
    t.commit()
for change in changes:
    print(change + (" (Simulated.)" if not commit else ""))
