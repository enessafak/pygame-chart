def check_all_number_in_list(lst):
    non_number_types = list(filter(lambda i: i not in (int, float), [type(i) for i in lst]))
    check = False if non_number_types else True
    return check

def check_list_xy(x,y):
    if type(x) == type(y) == list:
        if (check_all_number_in_list(x)) & (check_all_number_in_list(y)):
            if len(x) == len(y):
                return True
            else:
                raise KeyError('Length of x and y must be equal')
        else:
            raise KeyError('x and y can only include number types')
    else:
        raise KeyError('x and y can only be list type')