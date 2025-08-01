"""
Markdown XBlock tests
"""
from __future__ import print_function

import unittest

from mock import Mock, patch
from workbench.runtime import WorkbenchRuntime
from xblock.field_data import DictFieldData
from xblock.fields import ScopeIds

from markdown2 import MarkdownError

import markdown_xblock
from markdown_xblock.html import DEFAULT_EXTRAS


class TestMarkdownXBlock(unittest.TestCase):
    """
    Unit tests for `markdown_xblock`
    """
    def setUp(self):
        block_type = 'markdown'
        self.runtime = WorkbenchRuntime()
        def_id = self.runtime.id_generator.create_definition(block_type)
        usage_id = self.runtime.id_generator.create_usage(def_id)

        self.scope_ids = ScopeIds('user', block_type, def_id, usage_id)

    def test_render(self):
        """
        Test a basic rendering with default settings.
        """
        field_data = DictFieldData({'data': '# This is h1'})
        block = markdown_xblock.MarkdownXBlock(self.runtime, field_data, scope_ids=self.scope_ids)
        fragment = block.student_view()
        self.assertIn('<div class="markdown_xblock"><h1>This is h1</h1>\n</div>\n', fragment.content)

    def test_public_view(self):
        """
        Test public view rendering.
        """
        field_data = DictFieldData({'data': '# This is h1'})
        block = markdown_xblock.MarkdownXBlock(self.runtime, field_data, scope_ids=self.scope_ids)
        student_view_fragment = block.student_view()
        self.assertIn('<div class="markdown_xblock"><h1>This is h1</h1>\n</div>\n',
                      student_view_fragment.content)
        public_view_fragment = block.public_view()
        self.assertIn('<div class="markdown_xblock"><h1>This is h1</h1>\n</div>\n',
                      public_view_fragment.content)

    def test_render_default_settings(self):
        """
        Test a basic rendering with default settings.

        Expects the content to be sanitized by injecting
        [HTML_REMOVED] in place of the HTML tags, and the sentence
        being wrapped in a <p> block (since the <h1> tags are no
        longer interpreted as HTML).
        """
        field_data = DictFieldData({'data': '<h1>This is h1</h1>'})
        block = markdown_xblock.MarkdownXBlock(self.runtime, field_data, scope_ids=self.scope_ids)
        fragment = block.student_view()
        self.assertIn(
            '<div class="markdown_xblock"><p>[HTML_REMOVED]This is h1[HTML_REMOVED]</p>\n</div>\n',
            fragment.content
        )

    def test_render_invalid_safe_mode(self):
        """
        Test a basic rendering with default settings.

        Expects the rendering to fail since safe_mode is not set to
        one of 'replace', 'escape', True or False.
        """
        field_data = DictFieldData({'data': '<h1>This is h1</h1>'})
        block = markdown_xblock.MarkdownXBlock(self.runtime, field_data, scope_ids=self.scope_ids)
        settings = {
            "extras": DEFAULT_EXTRAS,
            "safe_mode": 'this is an invalid safe mode'
        }
        with patch('markdown_xblock.html.get_xblock_settings') as get_settings_mock:
            get_settings_mock.return_value = settings
            with self.assertRaises(MarkdownError):
                _ = block.student_view()

    def test_render_replace_inline_html(self):
        """
        Test a basic rendering with safe_mode explicitly set to 'replace'.

        Expects the content to be sanitized by injecting
        [HTML_REMOVED] in place of the HTML tags, and the sentence
        being wrapped in a <p> block (since the <h1> tags are no
        longer interpreted as HTML).
        """
        field_data = DictFieldData({'data': '<h1>This is h1</h1>'})
        block = markdown_xblock.MarkdownXBlock(self.runtime, field_data, scope_ids=self.scope_ids)
        settings = {
            "extras": DEFAULT_EXTRAS,
            "safe_mode": 'replace'
        }
        with patch('markdown_xblock.html.get_xblock_settings') as get_settings_mock:
            get_settings_mock.return_value = settings
            fragment = block.student_view()
            self.assertIn(
                '<div class="markdown_xblock"><p>[HTML_REMOVED]This is h1[HTML_REMOVED]</p>\n</div>\n',
                fragment.content
            )

    def test_render_replace_inline_html_boolean_setting(self):
        """
        Test a basic rendering with safe_mode set to True (instead of 'replace').

        Expects the content to be sanitized by injecting
        [HTML_REMOVED] in place of the HTML tags, and the sentence
        being wrapped in a <p> block (since the <h1> tags are no
        longer interpreted as HTML).
        """
        field_data = DictFieldData({'data': '<h1>This is h1</h1>'})
        block = markdown_xblock.MarkdownXBlock(self.runtime, field_data, scope_ids=self.scope_ids)
        settings = {
            "extras": DEFAULT_EXTRAS,
            "safe_mode": True
        }
        with patch('markdown_xblock.html.get_xblock_settings') as get_settings_mock:
            get_settings_mock.return_value = settings
            fragment = block.student_view()
            self.assertIn(
                '<div class="markdown_xblock"><p>[HTML_REMOVED]This is h1[HTML_REMOVED]</p>\n</div>\n',
                fragment.content
            )

    def test_render_escape_inline_html(self):
        """
        Test a basic rendering with safe_mode set to 'escape'

        Expects the content to be sanitized by escaping < and > with &lt; and &gt;
        and the sentence being wrapped in a <p> block (since the <h1> tags are
        no longer interpreted as HTML).
        """
        field_data = DictFieldData({'data': '<h1>This is h1</h1>'})
        block = markdown_xblock.MarkdownXBlock(self.runtime, field_data, scope_ids=self.scope_ids)
        settings = {
            "extras": DEFAULT_EXTRAS,
            "safe_mode": 'escape'
        }
        with patch('markdown_xblock.html.get_xblock_settings') as get_settings_mock:
            get_settings_mock.return_value = settings
            fragment = block.student_view()
            self.assertIn(
                '<div class="markdown_xblock"><p>&lt;h1&gt;This is h1&lt;/h1&gt;</p>\n</div>\n',
                fragment.content
            )

    def test_render_allow_inline_html(self):
        """
        Test a basic rendering with javascript enabled.
        Expects the content *not* to be sanitized.
        """
        field_data = DictFieldData({'data': '<h1>This is h1</h1>'})
        block = markdown_xblock.MarkdownXBlock(self.runtime, field_data, scope_ids=self.scope_ids)
        settings = {
            "extras": DEFAULT_EXTRAS,
            "safe_mode": False
        }
        with patch('markdown_xblock.html.get_xblock_settings') as get_settings_mock:
            get_settings_mock.return_value = settings
            fragment = block.student_view()
            self.assertIn('<div class="markdown_xblock"><h1>This is h1</h1>\n</div>\n',
                          fragment.content)

    def test_render_url_safe_mode_replace(self):
        """
        Test rendering a URL with safe_mode set to 'replace'.
        """
        field_data = DictFieldData(
            {'data': '[test1](https://test.com/courses/course-v1:Org+Class+Version/about) [test2](https://test.com/courses/course-v1%3AOrg%2BClass%2BVersion/about)'}  # noqa: E501
        )
        block = markdown_xblock.MarkdownXBlock(self.runtime, field_data, scope_ids=self.scope_ids)
        settings = {
            "extras": DEFAULT_EXTRAS,
            "safe_mode": 'replace'
        }
        with patch('markdown_xblock.html.get_xblock_settings') as get_settings_mock:
            get_settings_mock.return_value = settings
            fragment = block.student_view()
            self.assertIn(
                '<a href="https://test.com/courses/course-v1:Org+Class+Version/about">test1</a>',
                fragment.content
            )
            self.assertIn(
                '<a href="https://test.com/courses/course-v1%3AOrg%2BClass%2BVersion/about">test2</a>',
                fragment.content
            )

    def test_render_url_safe_mode_escape(self):
        """
        Test rendering a URL with safe_mode set to 'replace'.
        """
        field_data = DictFieldData(
            {'data': '[test1](https://test.com/courses/course-v1:Org+Class+Version/about) [test2](https://test.com/courses/course-v1%3AOrg%2BClass%2BVersion/about)'}  # noqa: E501
        )
        block = markdown_xblock.MarkdownXBlock(self.runtime, field_data, scope_ids=self.scope_ids)
        settings = {
            "extras": DEFAULT_EXTRAS,
            "safe_mode": 'escape'
        }
        with patch('markdown_xblock.html.get_xblock_settings') as get_settings_mock:
            get_settings_mock.return_value = settings
            fragment = block.student_view()
            self.assertIn(
                '<a href="https://test.com/courses/course-v1:Org+Class+Version/about">test1</a>',
                fragment.content
            )
            self.assertIn(
                '<a href="https://test.com/courses/course-v1%3AOrg%2BClass%2BVersion/about">test2</a>',
                fragment.content
            )

    def test_render_url_no_safe_mode(self):
        """
        Test rendering a URL with safe_mode disabled.
        """
        field_data = DictFieldData(
            {'data': '[test](https://test.com/courses/course-v1:Org+Class+Version/about)'}
        )
        block = markdown_xblock.MarkdownXBlock(self.runtime, field_data, scope_ids=self.scope_ids)
        settings = {
            "extras": DEFAULT_EXTRAS,
            "safe_mode": False
        }
        with patch('markdown_xblock.html.get_xblock_settings') as get_settings_mock:
            get_settings_mock.return_value = settings
            fragment = block.student_view()
            self.assertIn(
                '<a href="https://test.com/courses/course-v1:Org+Class+Version/about">test</a>',
                fragment.content
            )

    def test_substitution_no_system(self):
        """
        Test that the substitution is not performed when `system` is not present inside XBlock.
        """
        field_data = DictFieldData({'data': '%%USER_ID%% %%COURSE_ID%%'})
        block = markdown_xblock.MarkdownXBlock(self.runtime, field_data, scope_ids=self.scope_ids)
        fragment = block.student_view()
        self.assertIn('<div class="markdown_xblock"><p>%%USER_ID%% %%COURSE_ID%%</p>\n</div>\n', fragment.content)

    def test_substitution_not_found(self):
        """
        Test that the keywords are not replaced when they're not found.
        """
        field_data = DictFieldData({'data': 'USER_ID%% %%COURSE_ID%%'})
        block = markdown_xblock.MarkdownXBlock(self.runtime, field_data, scope_ids=self.scope_ids)
        block.system = Mock(anonymous_student_id=None)
        fragment = block.student_view()
        self.assertIn('<div class="markdown_xblock"><p>USER_ID%% %%COURSE_ID%%</p>\n</div>\n', fragment.content)

    def test_user_id_substitution(self):
        """
        Test replacing %%USER_ID%% with anonymous user ID.
        """
        field_data = DictFieldData({'data': '%%USER_ID%%'})
        block = markdown_xblock.MarkdownXBlock(self.runtime, field_data, scope_ids=self.scope_ids)
        block.system = Mock(anonymous_student_id='test_user')
        fragment = block.student_view()
        self.assertIn('<div class="markdown_xblock"><p>test_user</p>\n</div>\n', fragment.content)

    def test_course_id_substitution(self):
        """
        Test replacing %%COURSE_ID%% with HTML representation of course key.
        """
        field_data = DictFieldData({'data': '%%COURSE_ID%%'})
        block = markdown_xblock.MarkdownXBlock(self.runtime, field_data, scope_ids=self.scope_ids)
        course_locator_mock = Mock()
        course_locator_mock.html_id = Mock(return_value='test_course')
        block.system = Mock(course_id=course_locator_mock)
        fragment = block.student_view()
        self.assertIn('<div class="markdown_xblock"><p>test_course</p>\n</div>\n', fragment.content)
