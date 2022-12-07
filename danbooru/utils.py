def group_by(data, key):
    m = {}
    for d in data:
        k = key(d)
        if k in m:
            m[k].append(d)
        else:
            m[k] = [d]

    return m
