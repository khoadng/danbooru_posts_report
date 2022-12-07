from collections import Counter
from datetime import datetime

from danbooru.models.post import Post

LOCAL_TIMEZONE = datetime.now().astimezone().tzinfo

def frequency_report(posts: list[Post]):
    dates = [p.createdAt for p in posts]
    dates = [_to_local(d) for d in dates]
    date_of_weeks = [d.isoweekday() for d in dates]
    hours = [d.hour for d in dates]

    total_day = (dates[0] - dates[-1]).days
    p_per_day = len(dates) // total_day

    print(f'# Post per day: {p_per_day}')
    
    print('# Post count during week:')
    _date_of_week_report(date_of_weeks)

    print('# Post count during day:')
    _active_hour_report(hours)

def _to_local(date: datetime):
    return date.astimezone(LOCAL_TIMEZONE)

_int_to_date_dict = {
    1 : "Monday",
    2 : "Tuesday",
    3 : "Wednesday",
    4 : "Thursday",
    5 : "Friday",
    6 : "Saturday",
    7 : "Sunday",
}

def _active_hour_report(hours):
    counter = Counter(hours)
    counter_list = [(c, counter[c]) for c in counter]
    most_active = max(counter_list, key=lambda x: x[1])[0]
    least_active = min(counter_list, key=lambda x: x[1])[0]

    def __add_padding_hour(data: Counter):
        res = {d:data[d] for d in data}
        for h in range(24):
            if h not in res:
                res[h] = 0

        return res

    hours_dict = __add_padding_hour(counter)
    
    for c in sorted(hours_dict.keys()):
        most_active_text = "(most active)" if most_active == c else ""
        least_active_text = "(least active)" if least_active == c else ""
        active_text = most_active_text + least_active_text
        count = counter[c]
        print(f'{c:02}\'00:{_num_to_indicator(count, step=1)}')

def _date_of_week_report(date_of_weeks):
    counter = Counter(date_of_weeks)
    counter_list = [(c, counter[c]) for c in counter]
    # most_active = max(counter_list, key=lambda x: x[1])[0]
    # least_active = min(counter_list, key=lambda x: x[1])[0]
    
    for c in sorted(counter):
        date_text = _int_to_date_dict[c]
        date_text_short = date_text[:3]
        count = counter[c]
        # most_active_text = "(most active)" if most_active == c else ""
        # least_active_text = "(least active)" if least_active == c else ""
        # active_text = ''
        print(f'{date_text_short}:{_num_to_indicator(count, step=2)}')


def _num_to_indicator(num, step=2):
    total = num // step

    return f'({num: >3}) ' + ''.join(['|' for _ in range(total)])

if __name__ == "__main__":
    dates = [datetime.now()]
    # _date_of_week_report([1,2,2,2,2])
    # _active_hour_report([1,1,1,2,3,3])
    print(_num_to_indicator(1))
    print(_num_to_indicator(2))
    print(_num_to_indicator(20))
    print(_num_to_indicator(100))