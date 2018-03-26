def get_max_line_width(fragment):
    if not fragment:
        return 0
    bigger_line = max(fragment, key=len)
    return len(bigger_line)


def calculate_fragments_length_sum(fragments):
    return sum(map(len, fragments))
