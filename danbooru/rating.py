
from collections import Counter

from danbooru.models.post import Post

GENERAL = 'g'
SENSITIVE = 's'
QUESTIONABLE = 'q'
EXPLICIT = 'e'

nsfw_ratings = [
    SENSITIVE,
    QUESTIONABLE,
    EXPLICIT,
]

def rating_report(posts: list[Post]):
    ratings = [p.rating for p in posts]
    counter = Counter(ratings)
    total = counter.total()
    print('# Total rating count:')
    for c in counter:
        count = counter[c]
        print(f'{c}: {count: <3}')

    sfw_percent = round(counter[GENERAL] / total * 100, 2)
    nsfw_percent = round(100 - sfw_percent, 2)
    sexual_percent = round(counter[EXPLICIT] / total * 100, 2)

    print('# Content types:')
    print(f'SFW percent: {sfw_percent}%')
    print(f'NSFW percent: {nsfw_percent}%')
    print(f'Sexual percent: {sexual_percent}%')

if __name__ == "__main__":
    rating_report(['e','e','e','g','q','s', 's'])