# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from ruddocom.policy.testing import RUDDOCOM_POLICY_INTEGRATION_TESTING  # noqa
from zope.component import createObject, queryUtility

import unittest


try:
    from plone.dexterity.schema import portalTypeToSchemaName
except ImportError:
    # Plone < 5
    from plone.dexterity.utils import portalTypeToSchemaName


class PictureIntegrationTest(unittest.TestCase):

    layer = RUDDOCOM_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_picture_schema(self):
        fti = queryUtility(IDexterityFTI, name='Picture')
        schema = fti.lookupSchema()
        schema_name = portalTypeToSchemaName('Picture')
        self.assertIn(schema_name.lstrip('plone_0_'), schema.getName())

    def test_ct_picture_fti(self):
        fti = queryUtility(IDexterityFTI, name='Picture')
        self.assertTrue(fti)

    def test_ct_picture_factory(self):
        fti = queryUtility(IDexterityFTI, name='Picture')
        factory = fti.factory
        obj = createObject(factory)


    def test_ct_picture_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Picture',
            id='picture',
        )


        parent = obj.__parent__
        self.assertIn('picture', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('picture', parent.objectIds())

    def test_ct_picture_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Picture')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )
