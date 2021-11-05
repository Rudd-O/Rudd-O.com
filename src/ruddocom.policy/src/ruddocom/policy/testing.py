# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PLONE_FIXTURE,
    PloneSandboxLayer,
)
from plone.testing import z2

import ruddocom.policy


class RuddocomPolicyLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=ruddocom.policy)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ruddocom.policy:default')


RUDDOCOM_POLICY_FIXTURE = RuddocomPolicyLayer()


RUDDOCOM_POLICY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(RUDDOCOM_POLICY_FIXTURE,),
    name='RuddocomPolicyLayer:IntegrationTesting',
)


RUDDOCOM_POLICY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(RUDDOCOM_POLICY_FIXTURE,),
    name='RuddocomPolicyLayer:FunctionalTesting',
)


RUDDOCOM_POLICY_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        RUDDOCOM_POLICY_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='RuddocomPolicyLayer:AcceptanceTesting',
)
