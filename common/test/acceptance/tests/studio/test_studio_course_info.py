"""
Acceptance Tests for Course Information
"""
import uuid

from bok_choy.web_app_test import WebAppTest
from common.test.acceptance.pages.studio.course_info import CourseUpdatesPage
from flaky import flaky

from ...pages.studio.auto_auth import AutoAuthPage
from ...pages.studio.index import DashboardPage
from ...pages.studio.overview import CourseOutlinePage


def _create_course(self):
    """
    Helper method to create a course within the setup method
    """
    self.auth_page.visit()
    self.dashboard_page.visit()
    self.dashboard_page.wait_for_page()
    self.assertFalse(self.dashboard_page.has_course(
        org=self.course_org,
        number=self.course_number,
        run=self.course_run
    ))
    self.assertTrue(self.dashboard_page.new_course_button.present)
    self.dashboard_page.click_new_course_button()
    self.assertTrue(self.dashboard_page.is_new_course_form_visible())
    self.dashboard_page.fill_new_course_form(
        self.course_name,
        self.course_org,
        self.course_number,
        self.course_run
    )
    self.assertTrue(self.dashboard_page.is_new_course_form_valid())
    self.dashboard_page.submit_new_course_form()

    # Successful creation of course takes user to course outline page
    course_outline_page = CourseOutlinePage(
        self.browser,
        self.course_org,
        self.course_number,
        self.course_run
    )
    course_outline_page.visit()
    course_outline_page.wait_for_page()

    # Go back to dashboard and verify newly created course exists there
    self.dashboard_page.visit()
    self.assertTrue(self.dashboard_page.has_course(
        org=self.course_org, number=self.course_number, run=self.course_run
    ))


class UsersCanAddUpdatesTest(WebAppTest):
    """
      Scenario: Users can add updates
          Given I have opened a new course in Studio
          And I go to the course updates page
          When I add a new update with the text "Hello"
          Then I should see the update "Hello"
          And I see a "saving" notification
    """
    def setUp(self):
        super(UsersCanAddUpdatesTest, self).setUp()
        self.auth_page = AutoAuthPage(self.browser, staff=True)
        self.dashboard_page = DashboardPage(self.browser)

        self.course_name = "New Course Name" + str(uuid.uuid4().get_hex().upper()[0:6])
        self.course_org = "orgX"
        self.course_number = str(uuid.uuid4().get_hex().upper()[0:6])
        self.course_run = "2016_T2"

        # Create a course
        _create_course(self=self)
        self.course_updates_page = CourseUpdatesPage(
            self.browser,
            self.course_org,
            self.course_number,
            self.course_run
        )

    def test_course_updates_page_exists(self):
        self.course_updates_page.visit()
        self.course_updates_page.wait_for_page()
        self.assertTrue(self.course_updates_page.is_browser_on_page())
        self.assertTrue(self.course_updates_page.are_course_updates_on_page())
        self.assertTrue(self.course_updates_page.is_new_update_button_present)

    def test_new_course_update_is_present(self):
        self.course_updates_page.visit()
        self.assertTrue(self.course_updates_page.is_new_update_button_present())
        self.course_updates_page.click_new_update_button()
        self.assertTrue(self.course_updates_page.is_new_update_form_present())
        self.course_updates_page.submit_update('Hello')
        self.assertTrue(self.course_updates_page.update_text_contains('Hello'))


class UsersCanAddEditTest(WebAppTest):
    """
    Scenario: Users can edit updates
        Given I have opened a new course in Studio
        And I go to the course updates page
        When I add a new update with the text "Hello"
        And I modify the text to "Goodbye"
        Then I should see the update "Goodbye"
    """

    def setUp(self):
        super(UsersCanAddEditTest, self).setUp()
        self.auth_page = AutoAuthPage(self.browser, staff=True)
        self.dashboard_page = DashboardPage(self.browser)

        self.course_name = "New Course Name" + str(uuid.uuid4().get_hex().upper()[0:6])
        self.course_org = "orgX"
        self.course_number = str(uuid.uuid4().get_hex().upper()[0:6])
        self.course_run = "2016_T2"

        # Create a course
        _create_course(self=self)
        self.course_updates_page = CourseUpdatesPage(
            self.browser,
            self.course_org,
            self.course_number,
            self.course_run
        )

    def test_new_course_update_can_be_edited(self):
        self.course_updates_page.visit()
        self.assertTrue(self.course_updates_page.is_new_update_button_present())
        self.course_updates_page.click_new_update_button()
        self.assertTrue(self.course_updates_page.is_new_update_form_present())
        self.course_updates_page.submit_update('Hello')
        self.assertTrue(self.course_updates_page.update_text_contains('Hello'))
        self.assertTrue(self.course_updates_page.is_edit_button_present())
        self.course_updates_page.click_edit_update_button()
        self.course_updates_page.submit_update('Goodbye')
        self.assertFalse(self.course_updates_page.update_text_contains('Hello'))
        self.assertTrue(self.course_updates_page.update_text_contains('Goodbye'))


# On occasion this test will fail waiting for the update to be removed from the DOM
# Working to remove this issue in TNL-5051
@flaky(15, 15)
class UsersCanDeleteUpdateTest(WebAppTest):
    """
    Scenario: Users can delete updates
          Given I have opened a new course in Studio
          And I go to the course updates page
          And I add a new update with the text "Hello"
          And I delete the update
          And I confirm the prompt
          Then I should not see the update "Hello"
    """

    def setUp(self):
        super(UsersCanDeleteUpdateTest, self).setUp()
        self.auth_page = AutoAuthPage(self.browser, staff=True)
        self.dashboard_page = DashboardPage(self.browser)

        self.course_name = "New Course Name" + str(uuid.uuid4().get_hex().upper()[0:6])
        self.course_org = "orgX"
        self.course_number = str(uuid.uuid4().get_hex().upper()[0:6])
        self.course_run = "2016_T2"

        # Create a course
        _create_course(self=self)
        self.course_updates_page = CourseUpdatesPage(
            self.browser,
            self.course_org,
            self.course_number,
            self.course_run
        )

    def test_delete_course_update(self):
        self.course_updates_page.visit()
        self.assertTrue(self.course_updates_page.is_new_update_button_present())
        self.course_updates_page.click_new_update_button()
        self.assertTrue(self.course_updates_page.is_new_update_form_present())
        self.course_updates_page.submit_update('Hello')
        self.assertTrue(self.course_updates_page.update_text_contains('Hello'))
        self.course_updates_page.click_delete_update_button()
        self.course_updates_page.click_confirm_delete_action()
        self.assertFalse(self.course_updates_page.update_text_contains('Hello'))

class UsersCanEditUpdateDatesTest(WebAppTest):
    """
    Scenario: Users can edit update dates
        Given I have opened a new course in Studio
        And I go to the course updates page
        And I add a new update with the text "Hello"
        When I edit the date to "06/01/13"
        Then I should see the date "June 1, 2013"
    """

    def setUp(self):
        super(UsersCanEditUpdateDatesTest, self).setUp()
        self.auth_page = AutoAuthPage(self.browser, staff=True)
        self.dashboard_page = DashboardPage(self.browser)

        self.course_name = "New Course Name" + str(uuid.uuid4().get_hex().upper()[0:6])
        self.course_org = "orgX"
        self.course_number = str(uuid.uuid4().get_hex().upper()[0:6])
        self.course_run = "2016_T2"

        # Create a course
        _create_course(self=self)
        self.course_updates_page = CourseUpdatesPage(
            self.browser,
            self.course_org,
            self.course_number,
            self.course_run
        )

    def test_user_edit_update(self):
        self.course_updates_page.visit()
        self.assertTrue(self.course_updates_page.is_new_update_button_present())
        self.course_updates_page.click_new_update_button()
        self.assertTrue(self.course_updates_page.is_new_update_form_present())
        self.course_updates_page.submit_update('Hello')
        self.assertTrue(self.course_updates_page.update_text_contains('Hello'))
        self.course_updates_page.click_edit_update_button()
        self.course_updates_page.set_date('06/01/2013')
        self.course_updates_page.click_new_update_save_button()
        self.assertTrue(self.course_updates_page.is_saving_deleting_notification_present())
        self.assertTrue(self.course_updates_page.is_update_date('June 1, 2013'))


class TextOutsideTagsPreservedTest(WebAppTest):
    """
    Scenario: Text outside of tags is preserved
        Given I have opened a new course in Studio
        And I go to the course updates page
        When I add a new update with the text "before <strong>middle</strong> after"
        Then I should see the update "before <strong>middle</strong> after"
        And when I reload the page
        Then I should see the update "before <strong>middle</strong> after"
    """

    def setUp(self):
        super(TextOutsideTagsPreservedTest, self).setUp()
        self.auth_page = AutoAuthPage(self.browser, staff=True)
        self.dashboard_page = DashboardPage(self.browser)

        self.course_name = "New Course Name" + str(uuid.uuid4().get_hex().upper()[0:6])
        self.course_org = "orgX"
        self.course_number = str(uuid.uuid4().get_hex().upper()[0:6])
        self.course_run = "2016_T2"

        # Create a course
        _create_course(self=self)
        self.course_updates_page = CourseUpdatesPage(
            self.browser,
            self.course_org,
            self.course_number,
            self.course_run
        )

    def test_outside_tag_preserved(self):
        self.course_updates_page.visit()
        self.assertTrue(self.course_updates_page.is_new_update_button_present())
        self.course_updates_page.click_new_update_button()
        self.assertTrue(self.course_updates_page.is_new_update_form_present())
        self.course_updates_page.submit_update('before <strong>middle</strong> after')
        self.assertTrue(self.course_updates_page.update_text_contains('before <strong>middle</strong> after'))
        self.course_updates_page.visit()
        self.assertTrue(self.course_updates_page.update_text_contains('before <strong>middle</strong> after'))


class StaticLinksRewrittenWhenPreviewingCourseUpdateTest(WebAppTest):
    """
    Scenario: Static links are rewritten when previewing a course update
       Given I have opened a new course in Studio
       And I go to the course updates page
       When I add a new update with the text "<img src='/static/my_img.jpg'/>"
       # Can only do partial text matches because of the quotes with in quotes (and regexp step matching).
       Then I should see the asset update to "my_img.jpg"
       And I change the update from "/static/my_img.jpg" to "<img src='/static/modified.jpg'/>"
       Then I should see the asset update to "modified.jpg"
       And when I reload the page
       Then I should see the asset update to "modified.jpg"
    """

    def setUp(self):
        super(StaticLinksRewrittenWhenPreviewingCourseUpdateTest, self).setUp()
        self.auth_page = AutoAuthPage(self.browser, staff=True)
        self.dashboard_page = DashboardPage(self.browser)

        self.course_name = "New Course Name" + str(uuid.uuid4().get_hex().upper()[0:6])
        self.course_org = "orgX"
        self.course_number = str(uuid.uuid4().get_hex().upper()[0:6])
        self.course_run = "2016_T2"

        # Create a course
        _create_course(self=self)
        self.course_updates_page = CourseUpdatesPage(
            self.browser,
            self.course_org,
            self.course_number,
            self.course_run
        )

    def test_asset_change_in_updates(self):
        self.course_updates_page.visit()
        self.assertTrue(self.course_updates_page.is_new_update_button_present())
        self.course_updates_page.click_new_update_button()
        self.assertTrue(self.course_updates_page.is_new_update_form_present())
        self.course_updates_page.submit_update("<img src='/static/my_img.jpg'/>")
        self.assertTrue(self.course_updates_page.update_contains_html("my_img.jpg"))
        self.course_updates_page.click_edit_update_button()
        self.assertTrue(self.course_updates_page.is_new_update_form_present())
        self.course_updates_page.submit_update("<img src='/static/modified.jpg'/>")
        self.assertFalse(self.course_updates_page.update_contains_html("my_img.jpg"))
        self.assertTrue(self.course_updates_page.update_contains_html("modified.jpg"))
        self.course_updates_page.visit()
        self.assertTrue(self.course_updates_page.update_contains_html("modified.jpg"))
