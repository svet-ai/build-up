import datetime, time
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from widget_cards import Card, badge, heat, lbl, btn, row, NEON, DIM
from .base import Page

class ProfileScreen(Page):
    def build_ui(s):
        a = s.app; u = a.user; db = a.db; l = u['login']; W = (1, 1, 1, 1)
        pts = db.q('select points from users where login=?', (l,))[0]['points']; lvl = pts // 100 + 1
        hero = Card(hero=True); who = BoxLayout(orientation='vertical')
        who.add_widget(lbl(l, 22, W, True)); who.add_widget(lbl(f"{a.t('ent') if u['grade'] == 'ent' else u['grade'] + a.t('grade_n')} · {lvl} LVL", 13, (.9, .92, 1, 1)))
        hero.add_widget(row(badge(l[:2].upper(), (.72, .9, .83, 1), 64), who, h=70))
        tiles = BoxLayout(size_hint_y=None, height=dp(112), spacing=dp(8))
        for v, k in ((db.streak(l), 'streak'), (pts, 'points'), (f'#{db.rank(l)}', 'rank')):
            c = Card(); c.add_widget(lbl(v, 22, W, True)); c.add_widget(lbl(a.t(k), 11, DIM)); tiles.add_widget(c)
        hero.add_widget(tiles); s.box.add_widget(hero)
        t = datetime.date.today(); st = t - datetime.timedelta(days=t.weekday() + 21); cnt = db.daily(l, time.mktime(st.timetuple()))
        cells = [(cnt.get(st + datetime.timedelta(d), 0), st + datetime.timedelta(d) > t) for d in range(28)]
        c = Card(); c.add_widget(row(lbl(a.t('activity'), 18, W, True), lbl(a.t('last4'), 12, DIM), h=30)); c.add_widget(heat(cells, a.tr['wd'][['kk', 'ru', 'en'].index(a.lang)])); s.box.add_widget(c)
        s.box.add_widget(btn(a.t('grade'), lambda: a.go('grade'), False))
        s.box.add_widget(lbl(a.t('language'), 16, NEON, True))
        s.box.add_widget(row(*[btn(n, lambda l=l: a.set_lang(l), a.lang == l, 42) for l, n in (('kk', 'Қазақша'), ('ru', 'Русский'), ('en', 'English'))], h=42))
        if u['role'] == 'admin': s.box.add_widget(btn(a.t('admin'), lambda: a.go('admin')))
        s.box.add_widget(btn(f"{a.t('check_update')} (v{a.cfg['version']})", lambda: a.check_updates(True), False))
        s.box.add_widget(btn(a.t('logout'), a.logout, False))
