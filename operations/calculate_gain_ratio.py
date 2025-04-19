def calculate_gain_ratio(split_info, gain) -> float:
    try:
        return gain / split_info
    except ZeroDivisionError:
        return 0
