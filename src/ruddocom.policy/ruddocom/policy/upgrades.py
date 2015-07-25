from Products.CMFCore.utils import getToolByName

default_profile = 'profile-ruddocom.policy:default'

def upgrade_1_to_2(context):
    context.runImportStepFromProfile(default_profile, 'propertiestool')

def upgrade_2_to_3(context):
    context.runImportStepFromProfile(default_profile, 'ruddocom-cookiesettings')

def upgrade_3_to_4(context):
    context.runImportStepFromProfile(default_profile, 'cssregistry')

def upgrade_4_to_5(context):
    context.runImportStepFromProfile(default_profile, 'cssregistry')
