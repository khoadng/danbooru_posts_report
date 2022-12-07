import statistics

from danbooru.models.post import Post

def post(id):
    return f'https://danbooru.donmai.us/posts/{id}'

def print_rank(data, title, selector):
    print(f'# {title}:')

    for i, s in enumerate(data):
        rank = i + 1
        count = selector(s)
        print(f' {rank:<3}. {count:<4} -> ({post(s.id)})')

def _score_get(post: Post):
    return post.score

def _fav_get(post: Post):
    return post.fav_count

def _report(posts: list[Post], selector):
    sorted_posts = sorted(posts, reverse=True, key=selector)
    target_data = [selector(f) for f in sorted_posts]
    average = round(statistics.mean(target_data))
    median = statistics.median(target_data)

    print(f'average: {average}')
    print(f'median: {median}')

    best_sfw = [p for p in sorted_posts if p.rating == 'g']
    best_nsfw = [p for p in sorted_posts if p.rating != 'g']

    print_rank(best_sfw[:3], 'Best SFW', selector)
    print_rank(best_nsfw[:3], 'Best NSFW', selector)
    print_rank(sorted_posts[-3:], 'Worst', selector)

def score_report(posts: list[Post]):
    print('## SCORE')
    _report(posts, selector=_score_get)

def fav_report(posts: list[Post]):
    print('## FAVORITES')
    _report(posts, selector=_fav_get)


    