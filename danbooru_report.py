import json
import requests
import argparse

from danbooru.approve import approve_statistic_report, approver_report, ApproveData
from danbooru.fav_and_score import fav_report, score_report
from danbooru.models.post import Post
from danbooru.tag import tag_report
from danbooru.frequency import frequency_report
from danbooru.rating import rating_report
from danbooru.source import source_report
from danbooru.uploader import uploader_report

def create_request_url(login, api_key, tags, page=1, limit=200, age='<6m'):
    if login == None or api_key == None:
        return f'https://danbooru.donmai.us/posts.json?tags={tags}&age:{age}&limit={limit}&page={page}'

    return f'https://danbooru.donmai.us/posts.json?login={login}&api_key={api_key}&tags={tags}&age:{age}&limit={limit}&page={page}'
 
def create_request_user_url(ids):
    return f'https://danbooru.donmai.us/users.json?search[id]={",".join([str(id) for id in ids])}'

def request(url):
    res = requests.get(url)
    return json.loads(res.text)

def fetch_user(ids):
    url = create_request_user_url(ids)

    return request(url)

def fetch_post(url: str):
    json = request(url)
    posts = [
        Post(
            id=d['id'],
            createdAt=d['created_at'],
            fav_count=d['fav_count'],
            score=d['score'],
            rating=d['rating'],
            source=d['source'],
            uploader_id=d['uploader_id'],
            approver_id=d['approver_id'],
            is_pending=d['is_pending'],
            is_deleted=d['is_deleted'],
            tags=d['tag_string'].split(' '),
            artist_tags=d['tag_string_artist'].split(' '),
            character_tags=d['tag_string_character'].split(' '),
            copyright_tags=d['tag_string_copyright'].split(' '),
            general_tags=d['tag_string_general'].split(' '),
        ) 
        for d in json
    ]

    return posts

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Display tags statistic.')
    parser.add_argument('tag_string', type=str, 
                        help="A list of tags, space delimited")
    parser.add_argument('--login', action='store', type=str, help="Account name")
    parser.add_argument('--api_key', action='store', type=str, help="API key")
    parser.add_argument('--sample', action='store', type=int, help="Total posts")

    args = parser.parse_args()

    tags = args.tag_string
    login = args.login
    api_key = args.api_key
    sample = args.sample if args.sample != None else 400

    if (login != None and api_key == None) or (login == None and api_key != None):
        print("Must provide both API key and login")
        exit()


    total_page = max(sample // 200, 1)
    urls = [create_request_url(login, api_key, tags, page=i+1) for i in range(total_page)]

    data: list[Post] = []
    for url in urls:
        d = fetch_post(url)
        data += d
    
    # favcount = [(d['id'], d['fav_count'], post(d['id'])) for d in data]
    # score = [(d['id'], d['score'], post(d['id'])) for d in data]
    # createdAt = [(d['created_at']) for d in data]
    # rating = [(d['rating']) for d in data]
    # source = [(d['source']) for d in data]
    # uploader_id = [(d['uploader_id']) for d in data]
    # approve_data = [ApproveData(d['id'], d['approver_id'], d['rating']) for d in data if d['is_deleted'] == False]
    # pending = [d['id'] for d in data if d['is_pending'] == True]
    # deleted = [d['id'] for d in data if d['is_deleted'] == True]
    # tags = [t for d in data for t in d['tag_string'].split(' ')]
    # artists = [t for d in data for t in d['tag_string_artist'].split(' ')]
    # copyrights = [t for d in data for t in d['tag_string_copyright'].split(' ')]
    # characters = [t for d in data for t in d['tag_string_character'].split(' ')]
    # generals = [t for d in data for t in d['tag_string_general'].split(' ')]
    
    
    # favcount.sort(key=lambda x: x[1])
    # score.sort(key=lambda x: x[1])
    
    # favcount.reverse()
    # score.reverse()
    
    print('----')
    
    score_report(data)
    
    print('----')
    
    fav_report(data)
    
    print('----')
    
    approver_report([ApproveData(d.id, d.approver_id, d.rating) for d in data if d.is_deleted == False], user_fetcher=fetch_user)
    
    print('---')
    
    approve_statistic_report(data)
    
    print('---')
    
    frequency_report(data)
    
    print('---')
    
    rating_report(data)
    
    print('---')
    
    source_report(data)
    
    print('---')

    uploader_report(data, uploader_fetcher=fetch_user)

    print('---')
    
    print('Artists:')
    tag_report([d for p in data for d in p.artist_tags], len(data))
    print('>>>')
    
    print('Copyrights:')
    tag_report([d for p in data for d in p.copyright_tags], len(data))
    print('>>>')
    
    print('Characters:')
    tag_report([d for p in data for d in p.character_tags], len(data))
    print('>>>')
    