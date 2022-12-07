def group_by(data, key):
    m = {}
    for d in data:
        k = key(d)
        if k in m:
            m[k].append(d)
        else:
            m[k] = [d]

    return m


def num_to_indicator(num, step=2):
    total = num // step

    return f'({num: >3}) ' + ''.join(['|' for _ in range(total)])