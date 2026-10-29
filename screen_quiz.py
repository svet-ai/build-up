from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from service_calculator import calc
from widget_cards import Card, Ring, lbl, btn, row, bar, segs, NEON, GOOD, BAD, DIM
from screen_base import Page

class QuizScreen(Page):
    qs = []; done = False
    def start(s, qs, title, minutes):
        s.qs, s.title, s.i, s.ans, s.flag, s.done = qs, title, 0, {}, set(), False
        s.left = int(minutes * 60); s.stop(); s.ev = Clock.schedule_interval(s.tick, 1)
    def stop(s):
        if getattr(s, 'ev', None): s.ev.cancel(); s.ev = None
    def on_leave(s, *a): s.stop()
    def tick(s, dt):
        s.left -= 1
        if hasattr(s, 'tl'): s.tl.text = f'{s.left // 60:02d}:{s.left % 60:02d}'
        if s.left <= 0: s.finish()
    def build_ui(s):
        a = s.app
        if not s.qs: s.box.add_widget(lbl(a.t('no_q'), 18)); s.box.add_widget(btn(a.t('back'), lambda: a.go('home'))); return
        if s.done: return s.show_result()
        q = s.qs[s.i]; s.tl = lbl(f'{s.left // 60:02d}:{s.left % 60:02d}', 18, NEON, True)
        s.box.add_widget(row(lbl(f'{s.title}  {s.i + 1}/{len(s.qs)}', 14), s.tl, h=30)); s.box.add_widget(row(btn('Калькулятор', s.open_calc, False, 38), btn('Менделеев кестесі', s.open_periodic, False, 38), h=38)); s.box.add_widget(segs(len(s.qs), s.i, set(s.ans)))
        s.box.add_widget(lbl(f"{a.t('answered')} {len(s.ans)} · {a.t('left')} {len(s.qs) - len(s.ans)}", 13, DIM))
        c = Card(); c.add_widget(lbl(q['q'], 19, bold=True)); s.box.add_widget(c)
        for k, o in enumerate(q['o']):
            s.box.add_widget(btn(f"{'ABCD'[k]}.  {o}", lambda k=k: s.pick(k), s.ans.get(s.i) == k, 52))
        last = s.i == len(s.qs) - 1
        s.box.add_widget(row(btn(a.t('prev'), lambda: s.go(-1), False), btn('* ' + a.t('flag') if s.i in s.flag else a.t('flag'), s.toggle_flag, False),
                             btn(a.t('finish') if last else a.t('next'), s.finish if last else (lambda: s.go(1)))))
        if s.flag: s.box.add_widget(lbl('* ' + ', '.join(str(i + 1) for i in sorted(s.flag)), 13, NEON))
        s.box.add_widget(btn(a.t('finish'), s.finish, False, 40))
    def open_calc(s):
        root = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(8))
        display = TextInput(text='0', multiline=False, readonly=True, size_hint_y=None, height=dp(48), halign='right')
        root.add_widget(display); expr = ['']
        grid = GridLayout(cols=4, spacing=dp(4))
        keys = ['C','(',')','DEL','7','8','9','÷','4','5','6','×','1','2','3','-','0','.','^','+','sqrt(','sin(','cos(','tan(','ln(','log(','pi','=']
        def press(k):
            if k == 'C': expr[0] = ''
            elif k == 'DEL': expr[0] = expr[0][:-1]
            elif k == '=': expr[0] = calc(expr[0]) if expr[0] else ''
            else: expr[0] = ('' if expr[0] == 'Error' else expr[0]) + k
            display.text = expr[0] or '0'
        for k in keys: grid.add_widget(btn(k, lambda _k=k: press(_k), k in ('C','=') , 42))
        root.add_widget(grid); root.add_widget(btn('Жабу', lambda: pop.dismiss(), False, 40))
        pop = Popup(title='Калькулятор (тест кезінде)', content=root, size_hint=(.95,.85), auto_dismiss=True); pop.open()

    def open_periodic(s):
        import json, os
        from kivy.uix.gridlayout import GridLayout
        from kivy.uix.scrollview import ScrollView
        from kivy.uix.button import Button
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'periodic_table.json')
        elements = json.load(open(path, encoding='utf-8'))
        root = BoxLayout(orientation='vertical', spacing=dp(6), padding=dp(8))
        root.add_widget(lbl('Химиялық элементтер • 118 элемент', 16, NEON, True))
        sv = ScrollView(do_scroll_x=False); grid = GridLayout(cols=4, spacing=dp(4), size_hint_y=None, height=dp(((len(elements)+3)//4)*60))
        for e in elements:
            b = Button(text=f"{e['n']}  {e['s']}\n{e['name']}\n{e['m']}", font_size=dp(10), size_hint_y=None, height=dp(56), background_normal='', background_color=(.13,.22,.42,1))
            grid.add_widget(b)
        sv.add_widget(grid); root.add_widget(sv)
        root.add_widget(btn('Жабу', lambda: pop.dismiss(), False, 40))
        pop = Popup(title='Менделеев кестесі (тест кезінде)', content=root, size_hint=(.97,.92), auto_dismiss=True); pop.open()

    def pick(s, k): s.ans[s.i] = k; s.refresh()
    def go(s, d): s.i = max(0, min(len(s.qs) - 1, s.i + d)); s.refresh()
    def toggle_flag(s): s.flag ^= {s.i}; s.refresh()
    def finish(s):
        if s.done: return
        s.done = True; s.stop(); g = {}
        for i, q in enumerate(s.qs):
            c, t = g.get(q['s'], (0, 0)); g[q['s']] = (c + (s.ans.get(i) == q['a']), t + 1)
        s.pts = s.app.db.add_result(s.app.user['login'], g)
        for i, q in enumerate(s.qs): (s.app.db.del_mistake if s.ans.get(i) == q['a'] else s.app.db.add_mistake)(s.app.user['login'], q)
        s.refresh()
    def show_result(s):
        a = s.app; ok = sum(s.ans.get(i) == q['a'] for i, q in enumerate(s.qs)); pc = round(100 * ok / len(s.qs))
        col = GOOD if pc >= 60 else BAD; c = Card(acc=col)
        c.add_widget(row(Ring(pc / 100, f'{pc}%', f'{ok}/{len(s.qs)}', col), lbl(f"{a.t('result')}\n+{s.pts} {a.t('points')}", 22, NEON, True), h=140)); s.box.add_widget(c)
        wrong = []
        for i, q in enumerate(s.qs):
            good = s.ans.get(i) == q['a']
            if not good: wrong.append(q)
            c = Card(); c.add_widget(lbl(f"{i + 1}. {q['q']}", 15, bold=True))
            mine = q['o'][s.ans[i]] if i in s.ans else '—'
            c.add_widget(lbl(('+ ' if good else 'x ') + mine, 14, GOOD if good else BAD))
            if not good: c.add_widget(lbl(f"{a.t('right')}: {q['o'][q['a']]}", 14, GOOD))
            c.add_widget(lbl(f"{a.t('explain')}: {q['e']}", 13, (.7, .8, .95, 1))); s.box.add_widget(c)
        if wrong: s.box.add_widget(btn(a.t('retry'), lambda: a.quiz_with(wrong, s.title, max(1, len(wrong)))))
        s.box.add_widget(btn(a.t('home'), lambda: a.go('home'), False))
