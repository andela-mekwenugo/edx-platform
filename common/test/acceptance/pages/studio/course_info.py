"""
Course Updates page.
"""
from common.test.acceptance.pages.studio.utils import type_in_codemirror
from common.test.acceptance.pages.studio.utils import press_the_notification_button

from common.test.acceptance.pages.studio.course_page import CoursePage


class CourseUpdatesPage(CoursePage):
    """
    Course Updates page.
    """
    url_path = "course_info"

    def is_browser_on_page(self):
        return self.q(css='.handouts-content').present

    def are_course_updates_on_page(self):
        return self.q(css='article#course-update-view.course-updates').present

    def are_course_update_entries_present(self):
        return self.q(css='div.post-preview').present

    def is_new_update_button_present(self):
        return self.q(css='.new-update-button').present

    def click_new_update_button(self):
        # Wait for the handouts-content, otherwise the render of the page will clear the new update
        # form when loading content
        self.wait_for_element_presence('.handouts-content', '.handouts-content')
        self.q(css='.new-update-button').click()
        self.wait_for_element_visibility('.CodeMirror', 'Waiting for .CodeMirror')

    def is_new_update_form_present(self):
        return self.q(css='.CodeMirror').present

    def add_update(self, message):
        type_in_codemirror(self, 0, message)
        if self.is_new_update_save_button_present():
            self.click_new_update_save_button()

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
        self.wait_for_element_presence('.handouts-content', '.handouts-content')

    def click_delete_update_button(self):
        if self.is_delete_update_button_present():
            self.q(css='div.post-preview .delete-button').first.click()
            self.wait_for_page()

    def is_saving_deleting_notification_present(self):
        return self.q(css='.wrapper-notification-mini').present

    def update_text_contains(self, message):
        message_found = False
        updates = self.q(css='div.update-contents').html
        for update in updates:
            print update
            if update == message:
                message_found = True
        return message_found
