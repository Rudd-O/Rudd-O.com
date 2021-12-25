# -*- coding: utf-8 -*-
from plone import api
from plone.app.contenttypes.behaviors.leadimage import ILeadImage
from plone.app.layout.viewlets import ViewletBase


class LeadImageViewlet(ViewletBase):
    """A leadimage that never renders.
    
    Copied from plone.app.contenttypes.behaviors.viewlets.
    """

    def update(self):
        self.context = ILeadImage(self.context)
        self.available = False


class CustomLeadImageViewlet(ViewletBase):
    """A leadimage that renders an extra attribute "tall" or "wide".
    
    Copied from plone.app.contenttypes.behaviors.viewlets.
    """

    def update(self):
        self.context = ILeadImage(self.context)
        self.available = True if self.context.image else False
        self.aspect_ratio = "squarish"
        if self.available:
            width = getattr(self.context.image, "_width")
            height = getattr(self.context.image, "_height")
            if width and height:
                if height > (width * 1.3):
                    self.aspect_ratio = "tall"
                elif width > (height * 1.3):
                    self.aspect_ratio = "wide"

"""
 tal:define="scale_func context/@@images;
             scaled_image python: getattr(context.aq_explicit, 'image', False) and scale_func.scale('image', scale='large')"
             """
