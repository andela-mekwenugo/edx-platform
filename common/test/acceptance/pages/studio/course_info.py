"""
Course Updates page.
"""
from common.test.acceptance.pages.studio.course_page import CoursePage
from common.test.acceptance.pages.studio.utils import type_in_codemirror, set_input_value


class CourseUpdatesPage(CoursePage):
    """
    Course Updates page.
    """
    url_path = "course_info"

    def is_browser_on_page(self):
        """
        Returns whether or not the browser on the page and has loaded the required content
        """
        return self.q(css='.handouts-content').present

    def are_course_updates_on_page(self):
        """
        Is the course updates content Div loaded on the page
        """
        return self.q(css='article#course-update-view.course-updates').present

    def is_new_update_button_present(self):
        """
        Checks for the presence of the new update post button
        """
        return self.q(css='.new-update-button').present

    def click_new_update_button(self):
        """
        Wait for the handouts-content, otherwise the render of the page will clear the new update
        form when loading content
        """
        self.wait_for_element_presence('.handouts-content', '.handouts-content')
        self.q(css='.new-update-button').click()
        self.wait_for_page()
        self.wait_for_element_visibility('.CodeMirror', 'Waiting for .CodeMirror')

    def is_new_update_form_present(self):
        """
        Has the new update form loaded and it is present
        """
        return self.q(css='.CodeMirror').present

    def submit_update(self, message):
        """
        Adds update text to the new update CodeMirror form and submits that text

        Arguments:
            message (str): The message to be added and saved
        """
        type_in_codemirror(self, 0, message)
        if self.is_new_update_save_button_present():
            self.click_new_update_save_button()
            self.wait_for_page()

    def set_date(self, date):
        """
        Sets the updates date input to the provided value

        Arguments:
            date (str): Date string in the format DD/MM/YYYY
        """
        set_input_value(self, 'input.date', date)

    def is_update_date(self, search_date):
        """
        Checks to see if the search date is present

        Arguments:
            search_date (str): e.g. 06/01/2013 would be found with June 1, 2013
        """
        dates = self.q(css='.date-display').html
        for date in dates:
            if search_date == date:
                return True
        return False

    def is_new_update_save_button_present(self):
        """
        Checks to see if the CodeMirror Update save button is present
        """
        return self.q(css='.save-button').present

    def click_new_update_save_button(self):
        """
        Clicks the CodeMirror Update save button
        """
        self.q(css='.save-button').first.click()
        self.wait_for_page()

    def is_edit_button_present(self):
        """
        Checks to see if the edit update post buttons if present
        """
        return self.q(css='div.post-preview .edit-button').present

    def click_edit_update_button(self):
        """
        Clicks the edit update post button
        """
        self.q(css='div.post-preview .edit-button').first.click()
        self.wait_for_page()

    def is_delete_update_button_present(self):
        """
        Checks to see if the delete update post button is present
        """
        return self.q(css='div.post-preview .delete-button').present

    def click_confirm_delete_action(self):
        """
        Clicks the confirmation action when deleting a post
        """
        self.wait_for_element_visibility('button.action-primary', 'Waiting for the delete confirmation to be present')
        self.q(css='button.action-primary').first.click()
        self.wait_for_page()
        self.wait_for_ajax()
        # self.wait_for_element_absence('div.post-preview .update-contents',
        #                               'Waiting for the update-content to be cleared')

    def click_delete_update_button(self):
        """
        Clicks the delete update post button
        """
        self.wait_for_element_visibility('div.post-preview .delete-button', "Waiting for the delete buttons visibility")
        self.q(css='div.post-preview .delete-button').first.click()
        self.wait_for_page()

    def is_saving_deleting_notification_present(self):
        """
        Checks for the presence of the saving or deleting notification
        """
        return self.q(css='#notification-mini').present

    def update_text_contains(self, message):
        """
        Looks for the message in the list of updates in the page

        Arguments:
            message (str): String containing the message that is to be searched for

        Returns:
            bool: True if an instance of the message is found
        """
        updates = self.q(css='div.update-contents').html
        for update in updates:
            if update == message:
                return True
        return False

    def update_contains_html(self, value):
        """
        Looks for the html provided in all updates

        Arguments:
            value (str): String value that will be looked for

        Returns:
            bool: True if the value is contained in any of the update posts
        """
        updates = self.q(css='div.update-contents').html
        for update in updates:
            if value in update:
                return True
        return False
