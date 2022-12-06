from collections import Counter

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

def group_by(data, key):
    m = {}
    for d in data:
        k = key(d)
        if k in m:
            m[k].append(d)
        else:
            m[k] = [d]

    return m

def approve_statistic_report(pending, deleted, data):
    t_count = len(data)
    p_count = len(pending)
    d_count = len(deleted)
    a_count = t_count - p_count - d_count
    p_percent = round(p_count / t_count * 100, 2)
    d_percent = round(d_count / t_count * 100, 2)
    a_percent = round(a_count / t_count * 100, 2)

    print(f'Total: {t_count}')
    print(f'Active: {a_count}')
    print(f'Pending: {p_count}')
    print(f'Deleted: {d_count}')
    print(f'Active percent: {a_percent}%')
    print(f'Pending percent: {p_percent}%')
    print(f'Deleted percent: {d_percent}%')

def _calc_percent(num, total):
    return round(num / total * 100, 1)

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
