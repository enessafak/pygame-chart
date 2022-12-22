import math

def check_input_type(xdata, ydata):
    if type(xdata) == type(ydata) == list:
        return True
    else:
        raise KeyError('xdata and ydata must be list type!')

def check_input_length(xdata, ydata):
    if len(xdata) == len(ydata):
        return True
    else:
        raise KeyError('xdata and ydata must be the same length!')

def check_all_number(lst):
    non_number_types = list(filter(lambda i: i not in (int, float), [type(i) for i in lst]))
    check = False if non_number_types else True
    return check

def check_all_string(lst):
    non_string_types = list(filter(lambda i: i != str, [type(i) for i in lst]))
    check = False if non_string_types else True
    return check

def check_xy_data(xdata, ydata):
    if check_input_type(xdata, ydata):
        if check_input_length(xdata, ydata):
            if check_all_number(ydata):
                if check_all_number(xdata):
                    return True
                elif check_all_string(xdata):
                    return True
                else:
                    raise KeyError('xdata must include only number only string types!')
            else:
                raise KeyError('ydata must include only number types!')


def create_range(start, stop, step):
    lst = []
    i = start
    while True:
        if i > stop:
            break
        lst.append(i)
        i += step
    lst = [round(i, abs(math.floor(math.log10(step)))) for i in lst]
    return lst
