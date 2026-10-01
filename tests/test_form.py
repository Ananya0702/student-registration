import os
import unittest
from html.parser import HTMLParser

class HTMLTagParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.inputs = []
        self.selects = []
        self.textareas = []
        self.buttons = []
        self.forms = []
        self.title = ""
        self._inside_title = False

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        self.tags.append((tag, attr_dict))

        if tag == "title":
            self._inside_title = True
        elif tag == "form":
            self.forms.append(attr_dict)
        elif tag == "input":
            self.inputs.append(attr_dict)
        elif tag == "select":
            self.selects.append(attr_dict)
        elif tag == "textarea":
            self.textareas.append(attr_dict)
        elif tag == "button":
            self.buttons.append(attr_dict)

    def handle_endtag(self, tag):
        if tag == "title":
            self._inside_title = False

    def handle_data(self, data):
        if self._inside_title:
            self.title += data.strip()


class TestStudentRegistrationForm(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "index.html")
        )

        if os.path.exists(cls.html_path):
            with open(cls.html_path, "r", encoding="utf-8") as f:
                cls.html_content = f.read()
            cls.parser = HTMLTagParser()
            cls.parser.feed(cls.html_content)
        else:
            cls.html_content = None
            cls.parser = None

    def test_01_html_file_exists(self):
        """Test that index.html exists in the repository root."""
        self.assertTrue(
            os.path.exists(self.html_path),
            f"Missing file: {self.html_path} does not exist."
        )

    def test_02_html_is_not_empty(self):
        """Test that index.html has content."""
        self.assertIsNotNone(self.html_content, "index.html could not be read.")
        self.assertGreater(
            len(self.html_content.strip()),
            0,
            "index.html is empty."
        )

    def test_03_doctype_and_title(self):
        """Test that DOCTYPE and appropriate title tag are defined."""
        self.assertTrue(
            "<!DOCTYPE html>" in self.html_content or "<!doctype html>" in self.html_content.lower(),
            "HTML document is missing standard <!DOCTYPE html> declaration."
        )
        self.assertIn(
            "Student Registration",
            self.parser.title,
            f"Expected 'Student Registration' in title, got: '{self.parser.title}'"
        )

    def test_04_form_tag_exists(self):
        """Test that the <form> element exists with valid attributes."""
        self.assertGreaterEqual(
            len(self.parser.forms), 1, "No <form> tag found in index.html."
        )

    def test_05_name_input_field(self):
        """Test that Full Name input field exists."""
        name_fields = [
            inp for inp in self.parser.inputs
            if inp.get("name") in ["fullName", "name", "studentName"] or inp.get("id") in ["fullName", "name"]
        ]
        self.assertTrue(
            len(name_fields) > 0,
            "Missing 'Full Name' input field in form."
        )
        self.assertEqual(name_fields[0].get("type", "text"), "text")

    def test_06_email_input_field(self):
        """Test that Email input field exists with type='email'."""
        email_fields = [
            inp for inp in self.parser.inputs
            if inp.get("type") == "email" or "email" in inp.get("name", "").lower()
        ]
        self.assertTrue(
            len(email_fields) > 0,
            "Missing Email input field (type='email') in form."
        )

    def test_07_dob_input_field(self):
        """Test that Date of Birth input field exists with type='date'."""
        dob_fields = [
            inp for inp in self.parser.inputs
            if inp.get("type") == "date" or "dob" in inp.get("name", "").lower()
        ]
        self.assertTrue(
            len(dob_fields) > 0,
            "Missing Date of Birth field (type='date') in form."
        )

    def test_08_gender_radio_buttons(self):
        """Test that Gender radio buttons exist."""
        radio_fields = [
            inp for inp in self.parser.inputs
            if inp.get("type") == "radio" and inp.get("name") == "gender"
        ]
        self.assertGreaterEqual(
            len(radio_fields), 2,
            "Form must contain at least 2 radio button options for Gender."
        )

    def test_09_phone_input_field(self):
        """Test that Phone Number input field exists."""
        phone_fields = [
            inp for inp in self.parser.inputs
            if inp.get("type") == "tel" or "phone" in inp.get("name", "").lower()
        ]
        self.assertTrue(
            len(phone_fields) > 0,
            "Missing Phone Number field (type='tel' or name='phone') in form."
        )

    def test_10_course_select_dropdown(self):
        """Test that Course/Department select dropdown exists."""
        self.assertGreaterEqual(
            len(self.parser.selects),
            1,
            "Missing Course/Department <select> dropdown in form."
        )

    def test_11_address_textarea(self):
        """Test that Address textarea field exists."""
        self.assertGreaterEqual(
            len(self.parser.textareas),
            1,
            "Missing Address <textarea> field in form."
        )

    def test_12_submit_and_reset_buttons(self):
        """Test that Submit and Reset buttons exist."""
        all_buttons = self.parser.buttons + [
            inp for inp in self.parser.inputs if inp.get("type") in ["submit", "reset"]
        ]
        
        has_submit = any(
            btn.get("type") == "submit" or "submit" in btn.get("id", "").lower()
            for btn in all_buttons
        )
        has_reset = any(
            btn.get("type") == "reset" or "reset" in btn.get("id", "").lower()
            for btn in all_buttons
        )

        self.assertTrue(has_submit, "Missing Submit button in registration form.")
        self.assertTrue(has_reset, "Missing Reset button in registration form.")


if __name__ == "__main__":
    unittest.main()
