from ascii_engine.colors import RGB


def test_that_given_an_exact_rgb_it_returns_the_term_color():
    assert RGB(0, 0, 0).get_term_color() == 0
    assert RGB(95, 95, 255).get_term_color() == 63
    assert RGB(255, 0, 95).get_term_color() == 197


def test_that_given_a_not_mapped_color_it_should_return_by_proximity():
    assert RGB(13, 173, 214).get_term_color() == 38
    assert RGB(11, 22, 33).get_term_color() == 233
