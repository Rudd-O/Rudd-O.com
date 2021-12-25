# -*- coding: utf-8 -*-
from plone.app.contenttypes.behaviors.leadimage import ILeadImage
from plone.app.layout.viewlets import ViewletBase


class LeadImageViewlet(ViewletBase):
    """A leadimage that never renders."""

    def update(self):
        self.context = ILeadImage(self.context)
        self.available = False
