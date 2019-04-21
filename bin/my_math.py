def upper_clamp(input, clamp):
    if input > clamp:
        return clamp
    return input


def lower_clamp(input, clamp):
    if input < clamp:
        return clamp
    return input
