def approve_statistic_report(pending, deleted, data):
    t_count = len(data)
    p_count = len(pending)
    d_count = len(deleted)
    a_count = t_count - p_count - d_count
    p_percent = round(p_count / t_count * 100, 2)
    d_percent = round(d_count / t_count * 100, 2)
    a_percent = round(a_count / t_count * 100, 2)

    print(f'Total: {t_count}')
    print(f'Active: {a_count}')
    print(f'Pending: {p_count}')
    print(f'Deleted: {d_count}')
    print(f'Active percent: {a_percent}%')
    print(f'Pending percent: {p_percent}%')
    print(f'Deleted percent: {d_percent}%')

def approver_report(approver):
    dict = {}

    for a in approver:
        if a[1] not in dict:
            dict[a[1]] = [a[0]]
        else:
            item = 0 if a[0] == None else a[0]
            dict[a[1]].append(item)

    list = sorted([(str(k), dict[k]) for k in dict.keys()], reverse=True, key=lambda x: len(x[1]))

    for t in list:
        print(f'{t[0]: <6} ({len(t[1]): <2}) : {", ".join([str(i) for i in t[1]])}')