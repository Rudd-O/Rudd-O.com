from plone.app.multilingual.dx.interfaces import ILanguageIndependentField
from plone.namedfile import field
from plone.supermodel import model
from zope import schema
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
