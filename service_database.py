import sqlite3, os, hashlib, time, datetime

def data_dir():
    try:
        from kivy.app import App
        a = App.get_running_app()
        if a: return a.user_data_dir
    except Exception: pass
    return os.path.join(os.path.expanduser('~'), '.bilimup')

def hash_pw(pw, salt):
    return hashlib.pbkdf2_hmac('sha256', pw.encode(), bytes.fromhex(salt), 120000).hex()

class DB:
    def __init__(s, path=None):
        if path is None:
            os.makedirs(data_dir(), exist_ok=True); path = os.path.join(data_dir(), 'bilimup.db')
        s.c = sqlite3.connect(path); s.c.row_factory = sqlite3.Row
        s.c.executescript("""
        CREATE TABLE IF NOT EXISTS users(login TEXT PRIMARY KEY,salt TEXT,pw TEXT,role TEXT DEFAULT 'user',
          blocked INT DEFAULT 0,grade TEXT DEFAULT '',lang TEXT DEFAULT 'kk',points INT DEFAULT 0);
        CREATE TABLE IF NOT EXISTS results(id INTEGER PRIMARY KEY,login TEXT,subject TEXT,correct INT,total INT,tid REAL,ts REAL);
        CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY,data TEXT);
        CREATE TABLE IF NOT EXISTS mistakes(login TEXT,qtext TEXT,data TEXT,PRIMARY KEY(login,qtext));
        CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY,v TEXT);""")
        # Keep schema upgrades safe for existing installs.

    def q(s, sql, a=()):
        cur = s.c.execute(sql, a); s.c.commit(); return cur.fetchall()

    def set_session(s, login):
        if login: s.q("insert or replace into meta(k,v) values('remembered_login',?)", (login,))
        else: s.q("delete from meta where k='remembered_login'")

    def remembered_login(s):
        r = s.q("select v from meta where k='remembered_login'")
        return r[0]['v'] if r else None

    def user_by_login(s, login):
        r = s.q('select * from users where login=?', (login,))
        return dict(r[0]) if r and not r[0]['blocked'] else None

    def add_result(s, login, groups):
        """groups: {subject: (correct, total)}"""
        now = time.time(); pts = 0
        for sub, (c, t) in groups.items():
            s.q('insert into results(login,subject,correct,total,tid,ts) values(?,?,?,?,?,?)', (login, sub, c, t, now, now)); pts += c * 10
        s.q('update users set points=points+? where login=?', (pts, login)); return pts

    def summary(s, login):
        r = s.q('select count(distinct tid) n,coalesce(sum(correct),0) c,coalesce(sum(total),0) t from results where login=?', (login,))[0]
        return r['n'], r['c'], r['t']

    def by_subject(s, login):
        return s.q('select subject,sum(correct) c,sum(total) t from results where login=? group by subject', (login,))

    def history(s, login, n=10):
        return s.q('select tid,sum(correct) c,sum(total) t from results where login=? group by tid order by tid desc limit ?', (login, n))

    def since(s, login, days):
        d = datetime.date.today() - datetime.timedelta(days=days - 1)
        ts = time.mktime(d.timetuple())
        return s.q('select coalesce(sum(total),0) t from results where login=? and ts>=?', (login, ts))[0]['t']

    def streak(s, login):
        days = {datetime.date.fromtimestamp(r['ts']) for r in s.q('select ts from results where login=?', (login,))}
        d = datetime.date.today(); n = 0
        if d not in days: d -= datetime.timedelta(days=1)
        while d in days: n += 1; d -= datetime.timedelta(days=1)
        return n

    def leaderboard(s, n=10):
        return s.q("select login,points from users where role='user' and blocked=0 order by points desc limit ?", (n,))

    def add_mistake(s, login, q):
        import json; s.q('insert or replace into mistakes values(?,?,?)', (login, q['q'], json.dumps(q, ensure_ascii=False)))
    def del_mistake(s, login, q): s.q('delete from mistakes where login=? and qtext=?', (login, q['q']))
    def mistakes(s, login):
        import json; return [json.loads(r['data']) for r in s.q('select data from mistakes where login=?', (login,))]

    def rank(s, login):
        p = s.q('select points from users where login=?', (login,))[0]['points']
        return 1 + s.q("select count(*) n from users where role='user' and blocked=0 and points>?", (p,))[0]['n']

    def daily(s, login, start_ts):
        out = {}
        for r in s.q('select ts,total from results where login=? and ts>=?', (login, start_ts)):
            d = datetime.date.fromtimestamp(r['ts']); out[d] = out.get(d, 0) + r['total']
        return out
