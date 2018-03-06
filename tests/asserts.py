def assertPixelsAreEquals(pixels1, pixels2):
    pixels_list_1 = list(pixels1)
    pixels_list_2 = list(pixels2)

    assert len(pixels_list_1) == len(pixels_list_2)

    for line_1, line_2 in zip(pixels_list_1, pixels_list_2):
        assert list(line_1) == list(line_2)
