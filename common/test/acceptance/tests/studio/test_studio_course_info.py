"""
Acceptance Tests for Course Information
"""
from common.test.acceptance.pages.studio.course_info import CourseUpdatesPage

from base_studio_test import StudioCourseTest
from ...pages.studio.auto_auth import AutoAuthPage
from ...pages.studio.index import DashboardPage


class UsersCanAddUpdatesTest(StudioCourseTest):
    def setUp(self, is_staff=False, test_xss=True):
        super(UsersCanAddUpdatesTest, self).setUp()
        self.auth_page = AutoAuthPage(self.browser, staff=True)
        self.dashboard_page = DashboardPage(self.browser)

        self.course_name = self.course_info['display_name']
        self.course_org = self.course_info['org']
        self.course_number = self.course_info['number']
        self.course_run = self.course_info['run']

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
        """
          Scenario: Users can add updates
              Given I have opened a new course in Studio
              And I go to the course updates page
              When I add a new update with the text "Hello"
              Then I should see the update "Hello"
              And I see a "saving" notification
        """
        self.course_updates_page.visit()
        self.assertTrue(self.course_updates_page.is_new_update_button_present())
        self.course_updates_page.click_new_update_button()

        self.course_updates_page.submit_update('Hello')
        self.assertTrue(self.course_updates_page.update_text_contains('Hello'))

    def test_new_course_update_can_be_edited(self):
        """
        Scenario: Users can edit updates
            Given I have opened a new course in Studio
            And I go to the course updates page
            When I add a new update with the text "Hello"
            And I modify the text to "Goodbye"
            Then I should see the update "Goodbye"
        """

        self.course_updates_page.visit()
        self.assertTrue(self.course_updates_page.is_new_update_button_present())
        self.course_updates_page.click_new_update_button()

        self.course_updates_page.submit_update('Hello')
        self.assertTrue(self.course_updates_page.update_text_contains('Hello'))
        self.assertTrue(self.course_updates_page.is_edit_button_present())
        self.course_updates_page.click_edit_update_button()
        self.course_updates_page.submit_update('Goodbye')
        self.assertFalse(self.course_updates_page.update_text_contains('Hello'))
        self.assertTrue(self.course_updates_page.update_text_contains('Goodbye'))

    def test_delete_course_update(self):
        """
        Scenario: Users can delete updates
              Given I have opened a new course in Studio
              And I go to the course updates page
              And I add a new update with the text "Hello"
              And I delete the update
              And I confirm the prompt
              Then I should not see the update "Hello"
        """
        self.course_updates_page.visit()
        self.assertTrue(self.course_updates_page.is_new_update_button_present())
        self.course_updates_page.click_new_update_button()

        self.course_updates_page.submit_update('Hello')
        self.assertTrue(self.course_updates_page.update_text_contains('Hello'))
        self.course_updates_page.click_delete_update_button()
        self.assertFalse(self.course_updates_page.update_text_contains('Hello'))

    def test_user_edit_update(self):
        """
        Scenario: Users can edit update dates
            Given I have opened a new course in Studio
            And I go to the course updates page
            And I add a new update with the text "Hello"
            When I edit the date to "06/01/13"
            Then I should see the date "June 1, 2013"
        """
        self.course_updates_page.visit()
        self.assertTrue(self.course_updates_page.is_new_update_button_present())
        self.course_updates_page.click_new_update_button()

        self.course_updates_page.submit_update('Hello')
        self.assertTrue(self.course_updates_page.update_text_contains('Hello'))
        self.course_updates_page.click_edit_update_button()
        self.course_updates_page.set_date('06/01/2013')
        self.course_updates_page.click_new_update_save_button()
        self.assertTrue(self.course_updates_page.is_update_date('June 1, 2013'))

    def test_outside_tag_preserved(self):
        """
        Scenario: Text outside of tags is preserved
            Given I have opened a new course in Studio
            And I go to the course updates page
            When I add a new update with the text "before <strong>middle</strong> after"
            Then I should see the update "before <strong>middle</strong> after"
            And when I reload the page
            Then I should see the update "before <strong>middle</strong> after"
        """
        self.course_updates_page.visit()
        self.assertTrue(self.course_updates_page.is_new_update_button_present())
        self.course_updates_page.click_new_update_button()

        self.course_updates_page.submit_update('before <strong>middle</strong> after')
        self.assertTrue(self.course_updates_page.update_text_contains('before <strong>middle</strong> after'))
        self.course_updates_page.visit()
        self.assertTrue(self.course_updates_page.update_text_contains('before <strong>middle</strong> after'))

    def test_asset_change_in_updates(self):
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

        self.course_updates_page.visit()
        self.assertTrue(self.course_updates_page.is_new_update_button_present())
        self.course_updates_page.click_new_update_button()
        self.course_updates_page.submit_update("<img src='/static/my_img.jpg'/>")
        self.assertTrue(self.course_updates_page.update_contains_html("my_img.jpg"))
        self.course_updates_page.click_edit_update_button()
        self.course_updates_page.submit_update("<img src='/static/modified.jpg'/>")
        self.assertFalse(self.course_updates_page.update_contains_html("my_img.jpg"))
        self.assertTrue(self.course_updates_page.update_contains_html("modified.jpg"))
        self.course_updates_page.visit()
        self.assertTrue(self.course_updates_page.update_contains_html("modified.jpg"))
