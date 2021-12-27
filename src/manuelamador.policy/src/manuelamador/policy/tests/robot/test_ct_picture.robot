# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s manuelamador.policy -t test_picture.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src manuelamador.policy.testing.MANUELAMADOR_POLICY_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/manuelamador/policy/tests/robot/test_picture.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Picture
  Given a logged-in site administrator
    and an add Picture form
   When I type 'My Picture' into the title field
    and I submit the form
   Then a Picture with the title 'My Picture' has been created

Scenario: As a site administrator I can view a Picture
  Given a logged-in site administrator
    and a Picture 'My Picture'
   When I go to the Picture view
   Then I can see the Picture title 'My Picture'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Picture form
  Go To  ${PLONE_URL}/++add++Picture

a Picture 'My Picture'
  Create content  type=Picture  id=my-picture  title=My Picture

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Picture view
  Go To  ${PLONE_URL}/my-picture
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Picture with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Picture title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
