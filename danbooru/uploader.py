from collections import Counter

def uploader_report(uploader_ids, uploader_fetcher ):
    counter = Counter(uploader_ids)
    top_20 = counter.most_common(20)
    top_20_ids = [item[0] for item in top_20]
    uploaders = uploader_fetcher(top_20_ids)
    uploaders = [(u['id'], u['name']) for u in uploaders]
    print('Top 20 uploaders:')
    for i, c in enumerate(sorted(uploaders, key=lambda x: counter[x[0]], reverse=True)):
        rank = i + 1
        user_id = c[0]
        user_name = c[1]
      
        print(f' {rank:02}. {user_name: <20}: {counter[user_id]: <3}')
    


