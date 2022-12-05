from collections import Counter
from urllib.parse import urlparse


def source_report(sources_raw):
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
        print(f'{c: <20}: {count: <3}')
    
if __name__ == "__main__":
    source_report(["https://twitter.com/FELUCCACHAN/status/1592505739788324864", "https://i.pximg.net/img-zip-ugoira/img/2021/07/23/02/09/05/91429593_ugoira1920x1080.zip"])