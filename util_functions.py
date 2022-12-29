import math
from settings import *

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

def check_axis_limit(lim):
    if (type(lim) == tuple) & (len(lim) == 2):
        if lim[1] > lim[0]:
            if (type(lim[0]) in (int, float)) & (type(lim[1]) in (int, float)):
                return True
            else:
                raise Warning('Axis limit must be tuple of numbers for (min, max). Auto-calculated xlim is applied.')
        else:
            raise Warning('Axis max must be higher than axis min. Auto-calculated xlim is applied.')
    else:
        raise Warning('Axis limit must be tuple with two numbers. Auto-calculated xlim is applied.')


def create_range(start, stop):
    lst = []
    i = start
    while i < stop:
        lst.append(i)
        i += 1
    lst.append(i)
    return lst

def tick_range(mindata, maxdata):
    data_span = maxdata - mindata
    scale = 10 ** math.floor(math.log10(data_span))
    tick_size_normalized_list = [5.0, 2.0, 1.0, 0.5, 0.25, 0.1, 0.05, 0.02, 0.01]
    tick_size_normalized = 1.0
    for i in range(len(tick_size_normalized_list)):
        num_tick = data_span / scale / tick_size_normalized_list[i]
        if num_tick > MAX_TICK:
            tick_size_normalized = tick_size_normalized_list[i-1]
            break
    tick_size = tick_size_normalized * scale
    ticks = create_range(mindata/tick_size, maxdata/tick_size)
    ticks = [i * tick_size for i in [round(i) for i in ticks]]
    return ticks

