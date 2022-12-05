from collections import Counter


def tag_report(tags, total_post):
    counter = Counter(tags)
    tags = counter.most_common(10)
    total_tags = counter.total()
    average_tag_per_post = round(total_tags / total_post, 2)

    print(f'Total tags: {total_tags} from {total_post} posts')
    print(f'Average tags per post: {average_tag_per_post}')

    print(f'Top {len(tags)} tags:')
    for t in tags:
        tag = t[0] if t[0] != '' else '<empty>'
        print(f'{tag: <40}: {t[1]: <3} ({round(t[1] / total_tags * 100, 2): <4}%)')