from unittest.mock import MagicMock

from ascii_engine.elements.forms import InputField
from ascii_engine.fragments.converter import StringToPixelMatrixFragment


def test_that_it_renders_the_given_string():
    given_text = 'Hello, World!'
    input_field = InputField(
        InputField.State(given_text, False, 0)
    )

    assert isinstance(input_field.to_pixels(), StringToPixelMatrixFragment)
    assert ''.join(input_field.to_pixels().get_fragment()[0]) == given_text


def test_that_it_is_stylised_with_the_normal_style_when_not_focused():
    given_text = 'Hello, World!'
    input_field = InputField(
        InputField.State(given_text, False, 0)
    )

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
    input_field = InputField(
        InputField.State(given_text, True, 0)
    )

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
    input_field = InputField(
        InputField.State(given_text, True, 0)
    )

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
