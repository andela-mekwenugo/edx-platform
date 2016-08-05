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
        return self.q(css='.handouts-content').present

    def are_course_updates_on_page(self):
        return self.q(css='article#course-update-view.course-updates').present

    def is_new_update_button_present(self):
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
        return self.q(css='.CodeMirror').present

    def submit_update(self, message):
        type_in_codemirror(self, 0, message)
        if self.is_new_update_save_button_present():
            self.click_new_update_save_button()
            self.wait_for_page()

    def set_date(self, date):
        set_input_value(self, 'input.date', date)

    def is_update_date(self, search_date):
        dates = self.q(css='.date-display').html
        for date in dates:
            if search_date == date:
                return True
        return False

    def is_new_update_save_button_present(self):
        return self.q(css='.save-button').present

    def click_new_update_save_button(self):
        self.q(css='.save-button').first.click()
        self.wait_for_page()

    def is_edit_button_present(self):
        return self.q(css='div.post-preview .edit-button').present

    def click_edit_update_button(self):
        self.q(css='div.post-preview .edit-button').first.click()
        self.wait_for_page()

    def is_delete_update_button_present(self):
        return self.q(css='div.post-preview .delete-button').present

    def click_confirm_delete_action(self):
        self.q(css='button.action-primary').first.click()
        self.wait_for_ajax()
        self.wait_for_page()
        # self.wait_for_element_presence('.handouts-content', '.handouts-content')
        self.wait_for_element_absence('div.post-preview .update-contents',
                                      'Waiting for the update-content to be cleared')

    def click_delete_update_button(self):
        if self.is_delete_update_button_present():
            self.q(css='div.post-preview .delete-button').first.click()
            self.wait_for_page()

    def is_saving_deleting_notification_present(self):
        return self.q(css='#notification-mini').present

    def update_text_contains(self, message):
        updates = self.q(css='div.update-contents').html
        for update in updates:
            if update == message:
                return True
        return False

    def update_contains_html(self, value):
        updates = self.q(css='div.update-contents').html
        for update in updates:
            if value in update:
                return True
        return False
