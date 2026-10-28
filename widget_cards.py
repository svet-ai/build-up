import colorsys
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle, Line, Ellipse, Rectangle
from kivy.graphics.texture import Texture
from kivy.metrics import dp
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget

BG = (.02, .02, .05, 1); CARD = (.07, .07, .17, 1); PRI = (.36, .37, .88, 1); NEON = (.58, .6, 1, 1); DIM = (.66, .68, .84, 1)
HERO = (.3, .32, .89, 1); GOOD = (.37, .84, .63, 1); BAD = (1, .48, .52, 1); GOLD = (1, .64, .42, 1)
_n = [0]  # stagger counter, reset on every page refresh

def accent(i):
    r, g, b = colorsys.hsv_to_rgb((.5 + i * .13) % 1, .62, 1); return (r, g, b, 1)

def gradient_bg(w):
    """Vertical dark-blue gradient + soft neon glow behind the whole app."""
    t = Texture.create(size=(1, 2), colorfmt='rgba'); t.blit_buffer(bytes([3, 3, 9, 255, 12, 12, 36, 255]), colorfmt='rgba', bufferfmt='ubyte')
    t.mag_filter = 'linear'; t.wrap = 'clamp_to_edge'
    with w.canvas.before:
        Color(1, 1, 1, 1); r = Rectangle(texture=t)
        Color(PRI[0], PRI[1], PRI[2], .09); g = Ellipse()
    def u(*a):
        r.pos, r.size = w.pos, w.size; d = w.width * 1.2; g.size = (d, d); g.pos = (w.right - d * .7, w.top - d * .6)
    w.bind(pos=u, size=u)

class Card(BoxLayout):
    """Rounded card, colored accent stripe + outline, fades in one after another."""
    def __init__(s, **kw):
        hero = kw.pop('hero', False); acc = kw.pop('acc', None) or PRI; s._sw = 0 if hero else dp(5)
        kw.setdefault('orientation', 'vertical'); kw.setdefault('padding', [dp(16), dp(12), dp(12), dp(12)])
        kw.setdefault('spacing', dp(6)); kw.setdefault('size_hint_y', None)
        super().__init__(**kw); s.opacity = 0
        with s.canvas.before:
            Color(*(HERO if hero else CARD)); s._r = RoundedRectangle(radius=[dp(18)])
            Color(acc[0], acc[1], acc[2], 0 if hero else .9); s._a = RoundedRectangle(radius=[dp(18), 0, 0, dp(18)])
            Color(acc[0], acc[1], acc[2], .45); s._l = Line(rounded_rectangle=(0, 0, 1, 1, dp(18)), width=1.2)
        s.bind(pos=s._u, size=s._u, minimum_height=s.setter('height'))
        Clock.schedule_once(lambda dt: Animation(opacity=1, d=.4, t='out_quad').start(s), min(_n[0], 10) * .07); _n[0] += 1
    def _u(s, *a):
        s._r.pos, s._r.size = s.pos, s.size; s._a.pos, s._a.size = s.pos, (s._sw, s.height)
        s._l.rounded_rectangle = (s.x, s.y, s.width, s.height, dp(18))

class Ring(Widget):
    """Animated circular progress with a big value and a caption."""
    frac = NumericProperty(0)
    def __init__(s, frac, text='', sub='', color=NEON, **kw):
        super().__init__(size_hint=(None, None), size=(dp(130), dp(130)), **kw)
        with s.canvas:
            Color(.13, .21, .42, 1); s._bg = Line(width=dp(9), cap='round')
            Color(*color); s._fg = Line(width=dp(9), cap='round')
        s._t = Label(text=text, font_size=dp(26), bold=True); s._s = Label(text=sub, font_size=dp(11), color=DIM)
        s.add_widget(s._t); s.add_widget(s._s); s.bind(pos=s._u, size=s._u, frac=s._u)
        Animation(frac=max(0, min(frac, 1)), d=1.1, t='out_cubic').start(s)
    def _u(s, *a):
        cx, cy = s.center; r = s.width / 2 - dp(8)
        s._bg.circle = (cx, cy, r); s._fg.circle = (cx, cy, r, 0, max(.5, 360 * s.frac))
        s._t.center = (cx, cy + dp(8)); s._s.center = (cx, cy - dp(16))

def badge(text, col, size=46):
    L = Label(text=text, bold=True, font_size=dp(size * .45), color=(.02, .05, .12, 1), size_hint=(None, None), size=(dp(size), dp(size)))
    with L.canvas.before:
        Color(*col); e = Ellipse()
    L.bind(pos=lambda i, v: setattr(e, 'pos', v), size=lambda i, v: setattr(e, 'size', v)); return L

def lbl(text, size=15, color=(1, 1, 1, 1), bold=False, **kw):
    kw.setdefault('halign', 'left')
    L = Label(text=str(text), font_size=dp(size), color=color, bold=bold, size_hint_y=None, valign='middle', **kw)
    L.bind(width=lambda i, w: setattr(i, 'text_size', (w, None)), texture_size=lambda i, t: setattr(i, 'height', t[1] + dp(6)))
    return L

class PillButton(Button):
    def __init__(s, fill=None, outline=None, **kw):
        super().__init__(background_normal='', background_down='', background_color=(0, 0, 0, 0), **kw); s._f = s._o = None
        with s.canvas.before:
            if fill: Color(*fill); s._f = RoundedRectangle()
            if outline: Color(*outline); s._o = Line(width=dp(1.6))
        s.bind(pos=s._u, size=s._u)
    def _u(s, *a):
        r = s.height / 2
        if s._f: s._f.pos, s._f.size, s._f.radius = s.pos, s.size, [r]
        if s._o: s._o.rounded_rectangle = (s.x, s.y, s.width, s.height, r)

def btn(text, cb, primary=True, h=46, color=None):
    b = PillButton(color or (PRI if primary else None), None if primary else (.36, .38, .6, 1), text=text, size_hint_y=None, height=dp(h),
                   color=(1, 1, 1, 1), bold=True, halign='center')
    b.bind(width=lambda i, w: setattr(i, 'text_size', (w - dp(16), None)), on_press=lambda i: (Animation(opacity=.6, d=.06) + Animation(opacity=1, d=.15)).start(i))
    b.bind(on_release=lambda *_: cb()); return b

def chip(text):
    L = Label(text=text, font_size=dp(13), bold=True, size_hint=(None, None), height=dp(34))
    with L.canvas.before:
        Color(.1, .11, .45, .85); r = RoundedRectangle(radius=[dp(17)])
    L.bind(texture_size=lambda i, t: setattr(i, 'width', t[0] + dp(26)), pos=lambda i, v: setattr(r, 'pos', v), size=lambda i, v: setattr(r, 'size', v)); return L

def _cell(col):
    w = Widget()
    with w.canvas:
        c = Color(*col); r = RoundedRectangle(radius=[dp(7)])
    w.bind(pos=lambda i, v: setattr(r, 'pos', v), size=lambda i, v: setattr(r, 'size', v)); return w

def segs(n, cur, answered):
    b = BoxLayout(size_hint_y=None, height=dp(8), spacing=dp(5))
    for i in range(n): b.add_widget(_cell((.6, .62, 1, 1) if i == cur else PRI if i in answered else (.12, .13, .3, 1)))
    return b

def heat(cells, wd):
    """cells: 28 tuples (count, is_future); wd: 7 weekday labels."""
    box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(24 + 4 * 31), spacing=dp(4))
    h = GridLayout(cols=7, size_hint_y=None, height=dp(20))
    for x in wd: h.add_widget(Label(text=x, font_size=dp(12), color=DIM))
    g = GridLayout(cols=7, spacing=dp(5))
    for c, fut in cells:
        a = 0 if not c else .45 if c < 10 else .75 if c < 20 else 1
        w = _cell((PRI[0], PRI[1], PRI[2], a) if a else (.11, .12, .28, .4 if fut else 1)); g.add_widget(w)
    box.add_widget(h); box.add_widget(g); return box

def row(*ws, h=46):
    r = BoxLayout(size_hint_y=None, height=dp(h), spacing=dp(8))
    for w in ws: r.add_widget(w)
    return r

def bar(value, maximum=100):
    from kivy.uix.progressbar import ProgressBar
    p = ProgressBar(max=maximum, value=0, size_hint_y=None, height=dp(10)); Animation(value=min(value, maximum), d=.8, t='out_cubic').start(p); return p

def info(title, msg, ok='OK', cb=None):
    box = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(10))
    box.add_widget(lbl(msg, 16)); pop = Popup(title=title, content=box, size_hint=(.88, None), height=dp(260))
    box.add_widget(btn(ok, lambda: (pop.dismiss(), cb() if cb else None))); pop.open()
