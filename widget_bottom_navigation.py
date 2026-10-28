from kivy.animation import Animation
from kivy.graphics import Color, Line, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from .cards import CARD, PRI, DIM

ITEMS = ('home', 'subjects', 'progress', 'profile')

class BottomNav(BoxLayout):
    """Floating pill navigation: the active tab is a filled indigo pill."""
    def __init__(s, app, **kw):
        super().__init__(size_hint_y=None, height=dp(84), padding=[dp(12), dp(6), dp(12), dp(12)], **kw); s.app = app; s.b = {}; s.c = {}
        s.pill = BoxLayout(spacing=dp(4), padding=dp(6))
        with s.pill.canvas.before:
            Color(*CARD); s._r = RoundedRectangle(radius=[dp(34)]); Color(.22, .23, .42, 1); s._l = Line(width=1.5)
        s.pill.bind(pos=s._u, size=s._u); s.add_widget(s.pill)
        for k in ITEMS:
            b = Button(background_normal='', background_down='', background_color=(0, 0, 0, 0), color=DIM, bold=True, font_size=dp(12))
            with b.canvas.before:
                c = Color(PRI[0], PRI[1], PRI[2], 0); r = RoundedRectangle()
            b.bind(pos=lambda i, v, r=r: setattr(r, 'pos', v), size=lambda i, v, r=r: (setattr(r, 'size', v), setattr(r, 'radius', [v[1] / 2])))
            b.bind(on_release=lambda i, k=k: app.go(k)); s.b[k] = b; s.c[k] = c; s.pill.add_widget(b)
        s.retext()
    def _u(s, *a):
        s._r.pos, s._r.size = s.pill.pos, s.pill.size; s._l.rounded_rectangle = (*s.pill.pos, *s.pill.size, dp(34))
    def retext(s):
        for k, b in s.b.items(): b.text = s.app.t(k)
    def set_active(s, name):
        for k in ITEMS:
            Animation(a=1 if k == name else 0, d=.2).start(s.c[k]); Animation(color=(1, 1, 1, 1) if k == name else DIM, d=.2).start(s.b[k])
    def show(s, v):
        Animation(height=dp(84) if v else 0, opacity=1 if v else 0, d=.2).start(s)
