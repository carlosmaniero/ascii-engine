from ascii_engine.dimensions import Natural, Percentage


def test_that_a_natural_dimention_fits_inside_a_big_one():
    dimension = Natural(10)
    assert dimension.fits(100) == 10


def test_that_a_natural_dimension_is_never_bigger_than_the_given_size():
    dimension = Natural(45)
    assert dimension.fits(13) == 13


def test_that_the_percentage_fits_inside_a_number():
    assert Percentage(100).fits(13) == 13
    assert Percentage(40).fits(50) == 20
    assert Percentage(45).fits(13) == 5


def test_that_a_percentage_dimension_is_never_bigger_than_the_given_size():
    assert Percentage(120).fits(13) == 13
