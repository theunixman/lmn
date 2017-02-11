from django.test import TestCase

from lmn.forms import NewNoteForm
import string

# Test forms don't accept invalid data

class NewNoteFormTests(TestCase):

    def test_missing_title_is_invalid(self):
        form_data = { "text": "blah blah"};
        form = NewNoteForm(form_data)
        self.assertFalse(form.is_valid())

        invalid_titles = list(string.whitespace) + ['   ', '\n\n\n', '\t\t\n\t']

        for invalid_title in invalid_titles:
            form_data = { "title" : invalid_title , "text": "blah blah"};
            form = NewNoteForm(form_data)
            self.assertFalse(form.is_valid())


    def test_missing_text_is_invalid(self):
        form_data = { "title" : "blah blah" };
        form = NewNoteForm(form_data)
        self.assertFalse(form.is_valid())

        invalid_texts = list(string.whitespace) + ['   ', '\n\n\n', '\t\t\n\t']

        for invalid_text in invalid_texts:
            form_data = { "title": "blah blah", "text" : invalid_text};
            form = NewNoteForm(form_data)
            self.assertFalse(form.is_valid())



    def test_title_too_long_is_invalid(self):
        # Max length is 200
        form_data = { "title" : "a" * 201 };
        form = NewNoteForm(form_data)
        self.assertFalse(form.is_valid())


    def test_text_too_long_is_invalid(self):
        # Max length is 1000
        form_data = { "title" : "a" * 1001 };
        form = NewNoteForm(form_data)
        self.assertFalse(form.is_valid())


    def test_ok_title_and_length_is_valid(self):
        form_data = { "title": "blah blah", "text" : "blah, blah, blah."};
        form = NewNoteForm(form_data)
        self.assertTrue(form.is_valid())


class RegistrationFormTests(TestCase):
    pass

class LoginFormTests(TestCase):
    pass
