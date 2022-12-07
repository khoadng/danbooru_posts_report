import math

from collections import Counter
from danbooru.utils import num_to_indicator

def active_hour_report(hours):
    counter = Counter(hours)

    def __add_padding_hour(data: Counter):
        res = {d:data[d] for d in data}
        for h in range(24):
            if h not in res:
                res[h] = 0

        return res

    hours_dict = __add_padding_hour(counter)
    sample_size = len(hours)
    step = round(math.log10(sample_size))
    
    for c in sorted(hours_dict.keys()):
        count = counter[c]
        print(f'{c:02}\'00:{num_to_indicator(count, step=step)}')