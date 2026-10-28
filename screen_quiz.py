from kivy.clock import Clock
from kivy.metrics import dp
from widget_cards import Card, Ring, lbl, btn, row, bar, segs, NEON, GOOD, BAD, DIM
from .base import Page

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
        s.box.add_widget(row(lbl(f'{s.title}  {s.i + 1}/{len(s.qs)}', 14), s.tl, h=30)); s.box.add_widget(segs(len(s.qs), s.i, set(s.ans)))
        s.box.add_widget(lbl(f"{a.t('answered')} {len(s.ans)} · {a.t('left')} {len(s.qs) - len(s.ans)}", 13, DIM))
        c = Card(); c.add_widget(lbl(q['q'], 19, bold=True)); s.box.add_widget(c)
        for k, o in enumerate(q['o']):
            s.box.add_widget(btn(f"{'ABCD'[k]}.  {o}", lambda k=k: s.pick(k), s.ans.get(s.i) == k, 52))
        last = s.i == len(s.qs) - 1
        s.box.add_widget(row(btn(a.t('prev'), lambda: s.go(-1), False), btn('* ' + a.t('flag') if s.i in s.flag else a.t('flag'), s.toggle_flag, False),
                             btn(a.t('finish') if last else a.t('next'), s.finish if last else (lambda: s.go(1)))))
        if s.flag: s.box.add_widget(lbl('* ' + ', '.join(str(i + 1) for i in sorted(s.flag)), 13, NEON))
        s.box.add_widget(btn(a.t('finish'), s.finish, False, 40))
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
