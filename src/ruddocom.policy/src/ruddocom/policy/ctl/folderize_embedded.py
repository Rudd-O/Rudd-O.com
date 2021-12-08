#!/usr/bin/env python

import sys

import transaction
from zope.component.hooks import setSite
from plone import api


path = sys.argv[3]

obj = app.unrestrictedTraverse(path)
obj_id = obj.id
portal = obj.portal_url.getPortalObject()
setSite(portal)

parent = obj.aq_parent
folder = api.content.create(type='Folder', title=obj.title, container=parent)
obj = api.content.move(source=obj, target=folder, id="index")
folder = api.content.rename(folder, obj_id)
folder.setDefaultPage("index")

t = transaction.get()
t.note("Folderized %s" % path)
t.commit()
