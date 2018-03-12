from unittest.mock import Mock

from ascii_engine.colors import RGB


def test_that_given_an_exact_rgb_it_returns_the_term_color():
    assert RGB(0, 0, 0).calculate_term_color() == 0
    assert RGB(95, 95, 255).calculate_term_color() == 63
    assert RGB(255, 0, 95).calculate_term_color() == 197


def test_that_given_a_not_mapped_color_it_should_return_by_proximity():
    assert RGB(13, 173, 214).calculate_term_color() == 38
    assert RGB(11, 22, 33).calculate_term_color() == 233


def test_that_the_term_colors_stores_cache():
    RGB(13, 173, 214).calculate_term_color()
    assert RGB(13, 173, 214)._has_cache()


def test_that_the_term_colors_retrieves():
    color = RGB(13, 173, 214).calculate_term_color()
    assert RGB(13, 173, 214)._get_cached() == color


def test_that_calculate_term_colors_uses_the_cache():
    color = RGB(13, 173, 214)
    color._has_cache = Mock(return_value=True)
    color._get_cached = Mock(return_value=666)

    assert color.calculate_term_color() == 666
    assert color._has_cache.called
    assert color._get_cached.called
