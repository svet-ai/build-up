from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from widget_cards import Card, Ring, badge, accent, lbl, btn, bar, row, NEON, DIM, GOLD
from screen_base import Page

class HomeScreen(Page):
    def build_ui(s):
        a = s.app; u = a.user; db = a.db; l = u['login']
        pts = db.q('select points from users where login=?', (l,))[0]['points']; lvl, xp = pts // 100 + 1, pts % 100
        today = min(db.since(l, 1), 20); g = u['grade']
        s.box.add_widget(row(badge(l[:1].upper(), NEON, 48), BoxLayout(orientation='vertical'), h=50))
        s.box.children[0].children[0].add_widget(lbl(f"{a.t('hello')}, {l}!", 22, bold=True))
        s.box.children[0].children[0].add_widget(lbl(a.t('ent') if g == 'ent' else g + a.t('grade_n'), 13, DIM))
        hero = Card(acc=NEON); side = BoxLayout(orientation='vertical', spacing=dp(6))
        for w in (lbl(f'LVL {lvl}', 26, NEON, True), bar(xp, 100), lbl(f"{xp}/100 XP  ·  {pts} {a.t('points')}", 12, DIM), lbl(f"{a.t('streak')}: {db.streak(l)}", 16, GOLD, True)): side.add_widget(w)
        hero.add_widget(row(Ring(today / 20, f'{today}/20', a.t('goal')), side, h=140)); s.box.add_widget(hero)
        s.box.add_widget(btn(a.t('quick'), lambda: a.start_quiz(None, a.t('quick'), 10), True, 56))
        if g == 'ent':
            s.box.add_widget(lbl(a.t('directions'), 18, NEON, True))
            for i, (x, y) in enumerate(a.dirs):
                c = Card(acc=accent(i)); t = f'{a.sname(x)} – {a.sname(y)}'
                c.add_widget(row(badge(a.sname(x)[:1], accent(i)), lbl(t, 15, bold=True), btn(a.t('start'), lambda x=x, y=y, t=t: a.start_quiz([x, y], t, 20), True, 40), h=48)); s.box.add_widget(c)
        else:
            s.box.add_widget(lbl(a.t('subjects'), 18, NEON, True))
            for i, sub in enumerate([x for x in a.subjects if a.qs.count(x[0])][:6]):
                c = Card(acc=accent(i)); n = a.sname(sub[0])
                c.add_widget(row(badge(n[:1], accent(i)), lbl(n, 16, bold=True), btn(a.t('start'), lambda i=sub[0], n=n: a.start_quiz([i], n, 10), True, 40), h=48)); s.box.add_widget(c)
