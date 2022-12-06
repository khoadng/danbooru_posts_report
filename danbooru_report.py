import json

import requests

from danbooru.approve import approve_statistic_report, approver_report, ApproveData
from danbooru.fav_and_score import fav_report, score_report
from danbooru.tag import tag_report
from danbooru.frequency import frequency_report
from danbooru.rating import rating_report
from danbooru.source import source_report
from danbooru.uploader import uploader_report

import argparse


def post(id):
    return f'https://danbooru.donmai.us/posts/{id}'

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

    data = []
    for url in urls:
        d = request(url)
        data += d
    
    favcount = [(d['id'], d['fav_count'], post(d['id'])) for d in data]
    score = [(d['id'], d['score'], post(d['id'])) for d in data]
    createdAt = [(d['created_at']) for d in data]
    rating = [(d['rating']) for d in data]
    source = [(d['source']) for d in data]
    uploader_id = [(d['uploader_id']) for d in data]
    approve_data = [ApproveData(d['id'], d['approver_id'], d['rating']) for d in data if d['is_deleted'] == False]
    pending = [d['id'] for d in data if d['is_pending'] == True]
    deleted = [d['id'] for d in data if d['is_deleted'] == True]
    tags = [t for d in data for t in d['tag_string'].split(' ')]
    artists = [t for d in data for t in d['tag_string_artist'].split(' ')]
    copyrights = [t for d in data for t in d['tag_string_copyright'].split(' ')]
    characters = [t for d in data for t in d['tag_string_character'].split(' ')]
    generals = [t for d in data for t in d['tag_string_general'].split(' ')]
    
    
    favcount.sort(key=lambda x: x[1])
    score.sort(key=lambda x: x[1])
    
    favcount.reverse()
    score.reverse()
    
    print('----')
    
    score_report(score)
    
    print('----')
    
    fav_report(favcount)
    
    print('----')
    
    approver_report(approve_data, user_fetcher=fetch_user)
    
    print('---')
    
    approve_statistic_report(pending, deleted, data)
    
    print('---')
    
    frequency_report(createdAt)
    
    print('---')
    
    rating_report(rating)
    
    print('---')
    
    source_report(source)
    
    print('---')

    uploader_report(uploader_id, uploader_fetcher=fetch_user)

    print('---')
    
    print('Artists:')
    tag_report(artists, len(data))
    print('>>>')
    
    print('Copyrights:')
    tag_report(copyrights, len(data))
    print('>>>')
    
    print('Characters:')
    tag_report(characters, len(data))
    print('>>>')
    
    # print('General:')
    # tag_report(generals, len(data))
    # print('>>>')
    
    print('---')
