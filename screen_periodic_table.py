import colorsys, json, os
from kivy.metrics import dp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from widget_cards import btn, info, lbl, NEON
from .base import Page

def category(n):
    """Index into translations 'cat'."""
    if n in (3, 11, 19, 37, 55, 87): return 0
    if n in (4, 12, 20, 38, 56, 88): return 1
    if 57 <= n <= 71: return 2
    if 89 <= n <= 103: return 3
    if n in (9, 17, 35, 53, 85, 117): return 4
    if n in (2, 10, 18, 36, 54, 86, 118): return 5
    if n in (5, 14, 32, 33, 51, 52): return 6
    if n in (1, 6, 7, 8, 15, 16, 34): return 7
    return 8

def period(n): return next(i + 1 for i, e in enumerate((2, 10, 18, 36, 54, 86, 118)) if n <= e)

class PeriodicScreen(Page):
    def build_ui(s):
        a = s.app; base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        els = json.load(open(os.path.join(base, 'periodic_table.json'), encoding='utf-8'))
        s.box.add_widget(btn(a.t('back'), lambda: a.go('subjects'), False, 40)); s.box.add_widget(lbl(a.t('periodic') + ' (118)', 20, NEON, True))
        g = GridLayout(cols=5, spacing=dp(5), size_hint_y=None, height=dp(((len(els) + 4) // 5) * 62))
        for e in els:
            r, gr, b = colorsys.hsv_to_rgb(category(e['n']) / 9, .6, .55)
            b = Button(text=f"{e['s']}\n{e['n']}", background_normal='', background_color=(r, gr, b, 1), bold=True, halign='center')
            b.bind(on_release=lambda i, e=e: s.show(e)); g.add_widget(b)
        s.box.add_widget(g)
    def show(s, e):
        a = s.app; n = e['n']
        info(f"{e['s']} — {e['name']}", f"{a.t('number')}: {n}\n{a.t('mass')}: {e['m']}\n{a.t('period')}: {period(n)}\n{a.tr['cat'][category(n)][['kk', 'ru', 'en'].index(a.lang)]}", a.t('ok'))
