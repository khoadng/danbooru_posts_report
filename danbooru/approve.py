from collections import Counter
import datetime
from danbooru.active_hour import active_hour_report
from danbooru.danbooru_url_maker import post

from danbooru.models.post import Post
from danbooru.utils import group_by

class ApproveData:
    def __init__(self, pid, aid, rating):
        self.post_id = pid
        self.approver_id = aid
        self.rating = rating

class Approver:
    def __init__(self, id: int, name: str, approved_posts: list[ApproveData]):
        self.id = id
        self.name = name
        self.total_post_approved = len(list(approved_posts))
        self.approved_posts = approved_posts

def create_approver(id, name, approved: list[ApproveData]):
    return Approver(id, name, approved)

def _calc_percent(num, total):
    return round(num / total * 100, 1)

def approve_statistic_report(posts: list[Post]):
    t_count = len(posts)
    p_count = len([p.is_pending for p in posts if p.is_pending])
    d_count = len([p.is_deleted for p in posts if p.is_deleted])
    a_count = t_count - p_count - d_count
    p_percent = _calc_percent(p_count, t_count)
    d_percent = _calc_percent(d_count, t_count)
    a_percent = _calc_percent(a_count, t_count)

    print(f'Total: {t_count}')
    print(f'Active: {a_count}')
    print(f'Pending: {p_count}')
    print(f'Deleted: {d_count}')
    print(f'Active percent: {a_percent}%')
    print(f'Pending percent: {p_percent}%')
    print(f'Deleted percent: {d_percent}%')

    pendings = sorted([p for p in posts if p.is_pending == True], key=lambda x: x.createdAt)
    now = datetime.datetime.now()
    tz = now.tzinfo

    if pendings:
        print('# Pending:')
        for _, p in enumerate(pendings):
            pending_time = now.astimezone(tz) - p.createdAt.astimezone(tz)
            pending_hours = round(pending_time.total_seconds() / 60 / 60, 2)
            pending_day = round(pending_hours / 24, 2)
            if pending_hours < 24:
                print(f' {p.id}: {pending_hours} hours ago')
            else:
                print(f' {p.id}: {pending_day} days ago')


def approver_report(approve_data: list[ApproveData], user_fetcher):
    user_ids = [a.approver_id for a in approve_data]
    total = len(approve_data)
    approve_data_dict = group_by(approve_data, key=lambda x: x.approver_id)

    user_counter = Counter(user_ids)
    top_15 = [u[0] for u in user_counter.most_common(15) if u[0] != None]
    top_15_users = user_fetcher(top_15)

    approvers = [create_approver(u['id'], u['name'], approve_data_dict[u['id']]) for u in top_15_users] 

    print('# Top 15 approvers:')
    for i, approver in enumerate(sorted(approvers, key=lambda x: x.total_post_approved, reverse=True)):
        rank = i + 1
        total_approved_percent = round(approver.total_post_approved / total * 100, 2) 
        rating_counter = Counter([p.rating for p in approver.approved_posts])
        g_rating_count = rating_counter['g']
        s_rating_count = rating_counter['s']
        q_rating_count = rating_counter['q']
        e_rating_count = rating_counter['e']

        g_rating_percent = _calc_percent(g_rating_count, approver.total_post_approved)
        s_rating_percent = _calc_percent(s_rating_count, approver.total_post_approved)
        q_rating_percent = _calc_percent(q_rating_count, approver.total_post_approved)
        e_rating_percent = _calc_percent(e_rating_count, approver.total_post_approved)
      
        print(f' {rank:02}. {approver.name: <20}: {approver.total_post_approved: <3} ({g_rating_percent: <5}% | {s_rating_percent: <5}% | {q_rating_percent: <5}% | {e_rating_percent: <5}%) ({total_approved_percent}%)')


    approver_e_rating = [(a, len([p for p in a.approved_posts if p.rating == "e"])) for a in approvers]
    most_e_approved = max(approver_e_rating, key=lambda x: x[1])
    highest_e_approved = [(a[0] , _calc_percent(a[1], a[0].total_post_approved)) for a in approver_e_rating]
    highest_e_approved = max(highest_e_approved, key=lambda x: x[1])

    print(f'# Approver with most Explicit post approved: {most_e_approved[0].name} ({most_e_approved[1]})')
    print(f'# Approver with highest Explicit post approved: {highest_e_approved[0].name} ({highest_e_approved[1]}%)')


def approval_report(posts: list[Post]):
    approval_delays = [ (p, p.approved_at - p.createdAt) for p in posts if p.approved_at != None]
    approval_delays_group = group_by(approval_delays, key=lambda x: x[1].days)
    total = len(posts)

    day_key = sorted(approval_delays_group.keys())

    print('# Time for a post to be approved')
    for k in day_key:
        count = len(approval_delays_group[k])
        percent = _calc_percent(count, total)
        print(f'{k}: {count:>4} ({percent}%)')

    approved_late = day_key[3:]

    if approved_late:
        print('# Post got approved after deleted')
        for k in approved_late:
            print(f'- Day {k}:')
            for i, t in enumerate(approval_delays_group[k]):
                p, _ = t
                rank = i + 1
                print(f' {rank}. {post(p.id)} (rating: {p.rating})')

    print('# Approve hour during day:')
    hours = [p.approved_at.hour for p in posts if p.approved_at != None]
    active_hour_report(hours)
