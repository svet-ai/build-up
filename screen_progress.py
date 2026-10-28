import datetime
from widget_cards import Card, lbl, bar, row, NEON, DIM
from .base import Page

class ProgressScreen(Page):
    def build_ui(s):
        a = s.app; l = a.user['login']; db = a.db; n, c, t = db.summary(l)
        pts = db.q('select points from users where login=?', (l,))[0]['points']
        s.box.add_widget(lbl(a.t('progress'), 26, NEON, True))
        k = Card(); k.add_widget(row(lbl(f"{a.t('points')}\n{pts}", 16, bold=True), lbl(f"{a.t('tests')}\n{n}", 16, bold=True), lbl(f"{a.t('accuracy')}\n{round(100 * c / t) if t else 0}", 16, bold=True), h=60))
        k.add_widget(lbl(f"{a.t('week')}: {db.since(l, 7)}   {a.t('month')}: {db.since(l, 30)}   {a.t('streak')}: {db.streak(l)}", 13, DIM)); s.box.add_widget(k)
        for r in db.by_subject(l):
            b = Card(); b.add_widget(lbl(f"{a.sname(r['subject'])}: {round(100 * r['c'] / r['t'])}%", 14)); b.add_widget(bar(100 * r['c'] / r['t'])); s.box.add_widget(b)
        s.box.add_widget(lbl(a.t('rating'), 18, NEON, True)); rc = Card()
        for i, r in enumerate(db.leaderboard(10), 1): rc.add_widget(lbl(f"{i}. {r['login']} — {r['points']}", 15, NEON if r['login'] == l else (1, 1, 1, 1), r['login'] == l))
        s.box.add_widget(rc); s.box.add_widget(lbl(a.t('history'), 18, NEON, True)); hc = Card()
        for r in db.history(l): hc.add_widget(lbl(f"{datetime.datetime.fromtimestamp(r['tid']):%d.%m %H:%M}   {r['c']}/{r['t']}  ({round(100 * r['c'] / r['t'])}%)", 14))
        s.box.add_widget(hc)
