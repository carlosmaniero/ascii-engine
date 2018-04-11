from unittest.mock import MagicMock

from ascii_engine.colors import RGB
from ascii_engine.elements.forms import InputField
from ascii_engine.fragments.converter import StringToPixelMatrixFragment
from ascii_engine.pixel import Pixel


def test_that_it_renders_the_given_string():
    given_text = 'Hello, World!'
    input_field = InputField(InputField.State(given_text, False, 0))

    string_fragment = input_field.to_pixels()
    assert isinstance(
        string_fragment,
        StringToPixelMatrixFragment
    )
    assert ''.join(string_fragment.get_fragment()[0]) == given_text


def test_that_it_is_stylised_with_the_normal_style_when_not_focused():
    given_text = 'Hello, World!'
    input_field = InputField(InputField.State(given_text, False, 0))

    stubed_styles = [
        MagicMock(),
        MagicMock(),
        MagicMock(),
    ]

    input_field.set_style(stubed_styles)
    fragment = input_field.to_pixels()

    assert fragment == stubed_styles[2].return_value
    assert stubed_styles[0].called
    stubed_styles[1].assert_called_once_with(stubed_styles[0].return_value)
    stubed_styles[2].assert_called_once_with(stubed_styles[1].return_value)


def test_that_it_is_stylised_with_the_focused_style_when_not_focused():
    given_text = 'Hello, World!'
    input_field = InputField(InputField.State(given_text, True, 0))

    stubed_styles = [
        MagicMock(),
        MagicMock(),
        MagicMock(),
    ]

    input_field.set_focus_style(stubed_styles)
    fragment = input_field.to_pixels()

    assert fragment == stubed_styles[2].return_value
    assert stubed_styles[0].called
    stubed_styles[1].assert_called_once_with(stubed_styles[0].return_value)
    stubed_styles[2].assert_called_once_with(stubed_styles[1].return_value)


def test_that_it_is_stylised_with_the_focused_style_even_when_not_filled():
    given_text = ''
    input_field = InputField(InputField.State(given_text, True, 0))

    stubed_styles = [
        MagicMock(),
        MagicMock(),
        MagicMock(),
    ]

    input_field.set_focus_style(stubed_styles)
    fragment = input_field.to_pixels()

    assert fragment == stubed_styles[2].return_value
    assert stubed_styles[0].called
    stubed_styles[1].assert_called_once_with(stubed_styles[0].return_value)
    stubed_styles[2].assert_called_once_with(stubed_styles[1].return_value)


def test_that_it_is_stylised_with_the_normal_style_when_no_focus_style():
    given_text = 'Hello, World!'
    input_field = InputField(InputField.State(given_text, True, 0))

    stubed_styles = [
        MagicMock(),
        MagicMock(),
        MagicMock(),
    ]

    input_field.set_style(stubed_styles)
    fragment = input_field.to_pixels()

    assert fragment == stubed_styles[2].return_value
    assert stubed_styles[0].called
    stubed_styles[1].assert_called_once_with(stubed_styles[0].return_value)
    stubed_styles[2].assert_called_once_with(stubed_styles[1].return_value)


def test_that_it_is_stylised_with_the_placeholder_style_when_not_filled():
    given_text = ''
    input_field = InputField(InputField.State(given_text, True, 0))

    stubed_styles = [
        MagicMock(),
        MagicMock(),
        MagicMock(),
    ]

    input_field.set_placeholder_style(stubed_styles)
    fragment = input_field.to_pixels()

    assert fragment == stubed_styles[2].return_value
    assert stubed_styles[0].called
    stubed_styles[1].assert_called_once_with(stubed_styles[0].return_value)
    stubed_styles[2].assert_called_once_with(stubed_styles[1].return_value)


def test_that_it_is_stylised_with_the_normal_style_when_placeholder_not_set():
    given_text = ''
    input_field = InputField(InputField.State(given_text, True, 0))

    stubed_styles = [
        MagicMock(),
        MagicMock(),
        MagicMock(),
    ]

    input_field.set_style(stubed_styles)
    fragment = input_field.to_pixels()

    assert fragment == stubed_styles[2].return_value
    assert stubed_styles[0].called
    stubed_styles[1].assert_called_once_with(stubed_styles[0].return_value)
    stubed_styles[2].assert_called_once_with(stubed_styles[1].return_value)


def test_that_it_show_the_cursor_in_given_position():
    given_text = 'Hello, World!'
    given_bg = RGB(0, 0, 0)
    given_fg = RGB(255, 255, 255)
    input_field = InputField(
        InputField.State(given_text, True, 0),
        cursor_foreground=given_fg,
        cursor_background=given_bg
    )

    fragment = input_field.to_pixels()
    assert fragment[0][0] == Pixel('H', given_fg, given_bg)


def test_that_it_does_not_show_the_cursor_when_not_focused():
    given_text = 'Hello, World!'
    given_bg = RGB(0, 0, 0)
    given_fg = RGB(255, 255, 255)
    input_field = InputField(
        InputField.State(given_text, False, 0),
        cursor_foreground=given_fg,
        cursor_background=given_bg
    )

    fragment = input_field.to_pixels()
    assert fragment[0][0] == Pixel('H')
