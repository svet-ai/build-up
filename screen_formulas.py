import json, os
from widget_cards import Card, lbl, btn, NEON
from screen_base import Page

class FormulasScreen(Page):
    def build_ui(s):
        a = s.app; base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        s.box.add_widget(btn(a.t('back'), lambda: a.go('subjects'), False, 40)); s.box.add_widget(lbl(a.t('formulas'), 22, NEON, True))
        for f in json.load(open(os.path.join(base, 'formulas.json'), encoding='utf-8')):
            c = Card(); c.add_widget(lbl(f"{a.sname(f[0])}: {f[1 + ['kk', 'ru', 'en'].index(a.lang)]}", 14)); c.add_widget(lbl(f[4], 20, NEON, True)); s.box.add_widget(c)
