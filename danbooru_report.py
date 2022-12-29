import datetime
import json
import math
import time
import requests
import argparse

from danbooru.approve import approve_statistic_report, approver_report, approval_report, ApproveData
from danbooru.fav_and_score import  score_report
from danbooru.models.post import Post
from danbooru.tag import tag_report
from danbooru.frequency import frequency_report
from danbooru.rating import rating_report
from danbooru.source import source_report
from danbooru.uploader import uploader_report

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}

def create_request_url(login, api_key, tags, page=1, limit=200):
    if login == None or api_key == None:
        return f'https://danbooru.donmai.us/posts.json?tags={tags}&limit={limit}&page={page}'

    return f'https://danbooru.donmai.us/posts.json?login={login}&api_key={api_key}&tags={tags}&limit={limit}&page={page}'
 
def create_request_user_url(ids):
    return f'https://danbooru.donmai.us/users.json?search[id]={",".join([str(id) for id in ids])}'

def create_request_approval_url(ids):
    ids_string = ",".join([str(i) for i in ids])
    limit = len(ids)
    return f'https://danbooru.donmai.us/post_approvals.json?search[post_id]={ids_string}&limit={limit}'

def request(url):
    res = requests.get(url, headers=headers)
    return json.loads(res.text)

def fetch_user(ids):
    url = create_request_user_url(ids)

    return request(url)

def fetch_post(url: str):
    json = request(url)
    approved: list[int] = [d['id'] for d in json if d['is_deleted'] == False and d['is_pending'] == False]

    approval_json = request(create_request_approval_url(approved))
    approval_dict = {a['post_id']:a for a in approval_json}
    
    posts = [
        Post(
            id=d['id'],
            createdAt=datetime.datetime.fromisoformat(d['created_at']),
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
            approved_at= datetime.datetime.fromisoformat(approval_dict[d['id']]['created_at']) if d['id'] in approval_dict else None
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


    total_page = max(math.ceil(sample / 200), 1)
    urls = [(create_request_url(login, api_key, tags, page=i+1), i+1) for i in range(total_page)]

    data: list[Post] = []
    print(f'Total: {total_page} pages needed for {sample} posts')
    start = time.perf_counter()
    for t in urls:
        url, page = t
        print(f'Fetching page {page}')
        d = fetch_post(url)
        if not d:
            print(f'No data for page {page}, stopping...')
            break
        data += d

    end = time.perf_counter()
    elapsed = end - start
    
    print(f'Done in {elapsed:0.1f} seconds')
    
    print('---------------------------------')
    
    score_report(data)
    
    print('----')
    
    approver_report([ApproveData(d.id, d.approver_id, d.rating) for d in data if d.is_deleted == False], user_fetcher=fetch_user)
    
    print('---')
    
    approve_statistic_report(data)
    
    print('---')

    approval_report(data)

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
    