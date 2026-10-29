from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from widget_cards import Card, badge, accent, lbl, btn, row, DIM
from screen_base import Page
from screen_login import field

class SubjectsScreen(Page):
    def build_ui(s):
        a = s.app; labels = [f'{a.sname(x)} – {a.sname(y)}' for x, y in a.dirs]
        h = Card(hero=True); h.add_widget(lbl(a.t('mock'), 22, (1, 1, 1, 1), True))
        sp = Spinner(text=labels[0], values=labels, size_hint_y=None, height=dp(46), background_normal='', background_color=(.1, .11, .45, 1))
        h.add_widget(sp); h.add_widget(lbl(a.t('mock_hint'), 12, (.9, .92, 1, 1)))
        h.add_widget(btn(a.t('mock'), lambda: a.start_quiz(['kzhist', 'readlit', 'mathlit', *a.dirs[labels.index(sp.text)]], a.t('mock'), 40, 40), False, 46)); s.box.add_widget(h)
        for p in (('calculator', 'calc', 'periodic', 'periodic'), ('formulas', 'formulas', 'mistakes', 'mistakes')):
            s.box.add_widget(row(btn(a.t(p[0]), lambda n=p[1]: a.go(n), False, 42), btn(a.t(p[2]), lambda n=p[3]: a.go(n), False, 42), h=42))
        s.q = field(a.t('search')); s.q.bind(text=lambda *_: s.fill()); s.box.add_widget(s.q)
        s.list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(10)); s.list.bind(minimum_height=s.list.setter('height'))
        s.box.add_widget(s.list); s.fill()
    def fill(s):
        a = s.app; s.list.clear_widgets(); k = s.q.text.lower().strip()
        for i, sub in enumerate(a.subjects):
            if k and k not in ' '.join(sub[1:]).lower(): continue
            n = a.sname(sub[0]); cnt = a.qs.count(sub[0]); c = Card(acc=accent(i)); info = BoxLayout(orientation='vertical')
            info.add_widget(lbl(n, 16, bold=True)); info.add_widget(lbl(f"{a.t('tests')}: {cnt}", 12, DIM))
            c.add_widget(row(badge(n[:1], accent(i)), info, btn(a.t('start'), lambda i=sub[0], n=n: a.start_quiz([i], n, 10), True, 40) if cnt else lbl(a.t('no_q'), 12, DIM), h=52)); s.list.add_widget(c)
