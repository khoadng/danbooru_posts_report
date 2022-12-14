from collections import Counter
from datetime import datetime, timedelta
from danbooru.active_hour import active_hour_report

from danbooru.models.post import Post
from danbooru.utils import num_to_indicator

LOCAL_TIMEZONE = datetime.now().astimezone().tzinfo

def frequency_report(posts: list[Post]):
    dates = [p.createdAt for p in posts]
    dates = [_to_local(d) for d in dates]
    three_days = set(_get_inbetween_dates(datetime.now(), 3))
    seven_days = set(_get_inbetween_dates(datetime.now(), 7))
    thirty_days = set(_get_inbetween_dates(datetime.now(), 30))

    three_dates = [d for d in dates if datetime(d.year, d.month, d.day) in three_days]
    seven_dates = [d for d in dates if datetime(d.year, d.month, d.day) in seven_days]
    thirty_dates = [d for d in dates if datetime(d.year, d.month, d.day) in thirty_days]
    
    date_of_weeks = [d.isoweekday() for d in dates]
    hours = [d.hour for d in dates]

    total_day = (dates[0] - dates[-1]).days
    p_threedays = round(len(three_dates) / len(three_days), 1) 
    p_sevendays = round(len(seven_dates) / len(seven_days), 1)
    p_thirtydays = round(len(thirty_dates) / len(thirty_days), 1)
    p_alltimes = round(len(dates) / total_day, 1)

    print("# Frequency")
    print(f'Last 3 days : {p_threedays}/day')
    print(f'Last 7 days : {p_sevendays}/day')
    print(f'Last 30 days: {p_thirtydays}/day')
    print(f'All time    : {p_alltimes}/day')
    
    print('# Post count during week:')
    _date_of_week_report(date_of_weeks)

    print('# Post count during day:')
    active_hour_report(hours)

    print('# Post count during last 30 days:')
    _last_30_days_report([p.createdAt for p in posts])


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

def _date_of_week_report(date_of_weeks):
    counter = Counter(date_of_weeks)
    
    for c in sorted(counter):
        date_text = _int_to_date_dict[c]
        date_text_short = date_text[:3]
        count = counter[c]

        print(f'{date_text_short}:{num_to_indicator(count, step=2)}')

def _last_30_days_report(dates: list[datetime]):
    local_dates = [d.astimezone(LOCAL_TIMEZONE) for d in dates]
    dates_only = [datetime(d.year, d.month, d.day) for d in local_dates]
    counter = Counter(dates_only)

    thirty_days = _get_inbetween_dates(datetime.now(), 30)
    thirty_days_dict = {datetime(d.year, d.month, d.day):0 for d in thirty_days}
    for c in counter.keys():
        if c in thirty_days_dict:
            thirty_days_dict[c] = counter[c]

    counter = thirty_days_dict

    for d in sorted(counter.keys()):
        date_text = f'{d.day:02}/{d.month:02}/{d.year:02}'
        count = counter[d]
    
        print(f'{date_text}:{num_to_indicator(count, step=2)}')

def _get_inbetween_dates(start: datetime, total_days: int):
    end = start - timedelta(days=total_days)
    date_modified = start
    list=[start] 

    while date_modified > end:
        date_modified -= timedelta(days=1) 
        list.append(date_modified)

    return [datetime(d.year, d.month, d.day) for d in list]