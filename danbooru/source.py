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

    top_5 = counter.most_common(5)


    print('# Top 5 source')

    for c in top_5:
        count = c[1]
        name = c[0] if c[0] != None else "<None>"
        print(f'{name: <40}: {count: <3}')
