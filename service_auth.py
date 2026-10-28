import secrets
from .database import hash_pw

class Auth:
    def __init__(s, db): s.db = db

    def bootstrap_admin(s):
        """First launch: create admin with a random password (shown once, never stored in source)."""
        if s.db.q("select 1 from users where role='admin'"): return None
        pw = secrets.token_urlsafe(8); s.create('admin', pw, 'admin'); return pw

    def first_run_password(s):
        """Password to display on the login screen until the admin logs in for the first time."""
        if s.db.q("select 1 from meta where k='admin_seen'"): return None
        if s.db.q("select 1 from users where login='admin'"): return s.reset('admin')
        pw = secrets.token_urlsafe(8); s.create('admin', pw, 'admin'); return pw
    def mark_admin_seen(s): s.db.q("insert or replace into meta values('admin_seen','1')")

    def create(s, login, pw, role='user'):
        login = login.strip().lower()
        if not login or len(pw) < 6 or s.db.q('select 1 from users where login=?', (login,)): return False
        salt = secrets.token_hex(16)
        s.db.q('insert into users(login,salt,pw,role) values(?,?,?,?)', (login, salt, hash_pw(pw, salt), role)); return True

    def login(s, login, pw):
        r = s.db.q('select * from users where login=?', (login.strip().lower(),))
        if not r or secrets.compare_digest(hash_pw(pw, r[0]['salt']), r[0]['pw']) is False: return None, 'bad'
        return (None, 'blocked') if r[0]['blocked'] else (dict(r[0]), 'ok')

    def users(s): return s.db.q("select login,blocked,grade,points from users where role='user' order by login")
    def set_blocked(s, login, b): s.db.q('update users set blocked=? where login=?', (int(b), login))
    def reset(s, login):
        pw = secrets.token_urlsafe(6); salt = secrets.token_hex(16)
        s.db.q('update users set salt=?,pw=? where login=?', (salt, hash_pw(pw, salt), login)); return pw
    def update(s, login, **kw):
        for k, v in kw.items():
            if k in ('grade', 'lang'): s.db.q(f'update users set {k}=? where login=?', (v, login))
