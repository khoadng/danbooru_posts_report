import json

import requests

from danbooru.approve import approve_statistic_report, approver_report
from danbooru.fav_and_score import fav_report, score_report
from danbooru.tag import tag_report
from danbooru.frequency import frequency_report
from danbooru.rating import rating_report
from danbooru.source import source_report

import argparse


def post(id):
    return f'https://danbooru.donmai.us/posts/{id}'

def create_request_url(login, api_key, user, page=1, limit=200, age='<6m'):
    if login == None or api_key == None:
        return f'https://danbooru.donmai.us/posts.json?tags=user:{user}&age:{age}&limit={limit}&page={page}'

    return f'https://danbooru.donmai.us/posts.json?login={login}&api_key={api_key}&tags=user:{user}&age:{age}&limit={limit}&page={page}'
 

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Display uploader statistic.')
    parser.add_argument('uploader', type=str, 
                        help="Uploader's name")
    parser.add_argument('--login', action='store', type=str, help="Account name")
    parser.add_argument('--api_key', action='store', type=str, help="API key")

    args = parser.parse_args()

    user = args.uploader
    login = args.login
    api_key = args.api_key

    if (login != None and api_key == None) or (login == None and api_key != None):
        print("Must provide both API key and login")
        exit()

    url = create_request_url(login, api_key, user)
    url2 = create_request_url(login, api_key, user, page=2)
    
    res = requests.get(url)
    res2 = requests.get(url2)
    data = json.loads(res.text)
    data2 = json.loads(res2.text)
    data = data + data2
    
    favcount = [(d['id'], d['fav_count'], post(d['id'])) for d in data]
    score = [(d['id'], d['score'], post(d['id'])) for d in data]
    createdAt = [(d['created_at']) for d in data]
    rating = [(d['rating']) for d in data]
    source = [(d['source']) for d in data]
    approver = [(d['id'], d['approver_id']) for d in data if d['is_deleted'] == False]
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
    
    # approver_report(approver)
    
    # print('---')
    
    approve_statistic_report(pending, deleted, data)
    
    print('---')
    
    frequency_report(createdAt)
    
    print('---')
    
    rating_report(rating)
    
    print('---')
    
    source_report(source)
    
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
    
    print('General:')
    tag_report(generals, len(data))
    print('>>>')
    
    print('---')
    
    
    