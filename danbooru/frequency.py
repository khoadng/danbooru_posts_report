from collections import Counter
from datetime import datetime
from danbooru.active_hour import active_hour_report

from danbooru.models.post import Post
from danbooru.utils import num_to_indicator

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
    active_hour_report(hours)

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
