def score_report(score):
    score_sorted = sorted(score, reverse=True, key=lambda x: x[1])
    average = sum([f[1] for f in score]) // len(score)

    print(f'average score: {average}')
    print(f'top 1 score: {score_sorted[0]}')
    print(f'top 2 score: {score_sorted[1]}')
    print(f'top 3 score: {score_sorted[2]}')
    print(f'lowest score: {min(score, key= lambda x: x[1])}')

def fav_report(favcount):
    fav_sorted = sorted(favcount, reverse=True, key=lambda x: x[1])
    average = sum([f[1] for f in favcount]) // len(favcount)

    print(f'average favorite: {average}')
    print(f'top 1 favorite: {fav_sorted[0]}')
    print(f'top 2 favorite: {fav_sorted[1]}')
    print(f'top 3 favorite: {fav_sorted[2]}')
    print(f'lowest favorite: {min(favcount, key= lambda x: x[1])}')