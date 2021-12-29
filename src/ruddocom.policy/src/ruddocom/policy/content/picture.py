from Products.CMFPlone.browser.syndication.adapters import DexterityItem
from Products.CMFPlone.interfaces.syndication import IFeed
from plone.app.multilingual.dx.interfaces import ILanguageIndependentField
from plone.dexterity.content import Item
from plone.namedfile import field
from plone.supermodel import model
from zope import schema
from zope.component import adapts
from zope.interface import alsoProvides


class IPicture(model.Schema):
    """Marker interface for Picture"""

    picture = field.NamedBlobImage(
        description="The picture",
        title="Picture",
    )

    source = schema.URI(
        description="The source for this picture",
        title="Source",
        required=False,
    )


alsoProvides(IPicture["picture"], ILanguageIndependentField)
alsoProvides(IPicture["source"], ILanguageIndependentField)


class Picture(Item):

    @property
    def image(self):
        return self.picture


class PictureAdapter(DexterityItem):
    adapts(IPicture, IFeed)

    @property
    def has_enclosure(self):
        return True

    @property
    def file_length(self):
        return self.context.picture.size

    @property
    def file_type(self):
        return self.context.picture.contentType

    @property
    def file_url(self):
        return "{}/@@display-file/picture/{}".format(self.base_url, self.context.picture.filename)

    guid = file_url

    @property
    def file(self):
        return self.context.picture
