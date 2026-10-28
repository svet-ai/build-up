import json, os, random

class QuestionService:
    def __init__(s, base, db):
        s.db = db
        with open(os.path.join(base, 'questions.json'), encoding='utf-8') as f: s.base = json.load(f)

    def all(s): return s.base + [json.loads(r['data']) for r in s.db.q('select data from questions')]
    def count(s, sid): return sum(1 for q in s.all() if q['s'] == sid)

    def mix(s, sids=None, n=10):
        pool = [q for q in s.all() if not sids or q['s'] in sids]; out = []
        for q in random.sample(pool, min(n, len(pool))):
            o = list(enumerate(q['o'])); random.shuffle(o)
            out.append({'s': q['s'], 'q': q['q'], 'o': [x[1] for x in o], 'a': [x[0] for x in o].index(q['a']), 'e': q.get('e', '')})
        return out

    def add(s, sid, text, opts, a, e=''):
        opts = [o.strip() for o in opts]
        if not text.strip() or len(opts) != 4 or not all(opts) or len(set(opts)) != 4 or a not in range(4): return False
        s.db.q('insert into questions(data) values(?)', (json.dumps({'s': sid, 'q': text.strip(), 'o': opts, 'a': a, 'e': e}, ensure_ascii=False),)); return True

    def merge(s, items):
        have = {q['q'] for q in s.all()}; n = 0
        for x in items:
            try:
                if x['q'] not in have and s.add(x['s'], x['q'], x['o'], x['a'], x.get('e', '')): have.add(x['q']); n += 1
            except (KeyError, TypeError): pass
        return n
