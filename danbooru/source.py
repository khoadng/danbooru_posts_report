from collections import Counter
from urllib.parse import urlparse

from danbooru.models.post import Post

def source_report(posts: list[Post]):
    sources_raw = [p.source for p in posts]
    sources = [urlparse(s) for s in sources_raw]
    hosts = [s.hostname for s in sources]

    counter = Counter(hosts)
    most_common_host = counter.most_common()[0]
    most_common_percent = round(most_common_host[1] / len(hosts) * 100, 2)

    print(f'Most common source: {most_common_host[0]} ({most_common_percent}%)')

    print('# Source')

    for c in counter:
        count = counter[c]
        # source_string = 'pixiv.net' if c == 'i.pximg.net' else c
        print(f'{c if c != None else "<None>": <20}: {count: <3}')
