from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from widget_cards import Card, lbl, btn, row, info, NEON, BAD
from .base import Page
from .login import field

class AdminScreen(Page):
    def build_ui(s):
        a = s.app; s.box.add_widget(lbl(a.t('admin'), 24, NEON, True)); s.box.add_widget(btn(a.t('back'), lambda: a.go('profile'), False, 40))
        c = Card(); s.nl, s.np = field(a.t('login')), field(a.t('temp_pw'))
        for w in (s.nl, s.np, btn(a.t('create'), s.create)): c.add_widget(w)
        s.box.add_widget(c)
        for u in a.auth.users():
            c = Card(); c.add_widget(lbl(f"{u['login']}   ({u['points']} {a.t('points')})" + ('  [X]' if u['blocked'] else ''), 15, BAD if u['blocked'] else (1, 1, 1, 1), True))
            c.add_widget(row(btn(a.t('unblock') if u['blocked'] else a.t('block'), lambda l=u['login'], b=u['blocked']: s.block(l, not b), False, 38),
                             btn(a.t('reset'), lambda l=u['login']: s.reset(l), False, 38), h=38)); s.box.add_widget(c)
        s.box.add_widget(lbl(a.t('add_q'), 18, NEON, True)); c = Card()
        s.sp = Spinner(text=a.subjects[0][0], values=[x[0] for x in a.subjects], size_hint_y=None, height=dp(42))
        s.qt = field(a.t('question')); s.qo = [field(f"{a.t('option')} {i + 1}") for i in range(4)]; s.qa = field(a.t('correct_idx')); s.qe = field(a.t('explain'))
        for w in [s.sp, s.qt, *s.qo, s.qa, s.qe, btn(a.t('save'), s.addq)]: c.add_widget(w)
        s.box.add_widget(c)
    def create(s):
        a = s.app
        if len(s.np.text) < 6: return info(a.t('admin'), a.t('min6'), a.t('ok'))
        ok = a.auth.create(s.nl.text, s.np.text); info(a.t('admin'), a.t('saved') if ok else a.t('invalid'), a.t('ok')); s.refresh()
    def block(s, l, b): s.app.auth.set_blocked(l, b); s.refresh()
    def reset(s, l): info(l, f"{s.app.t('temp_pw')}: {s.app.auth.reset(l)}", s.app.t('ok'))
    def addq(s):
        a = s.app; idx = int(s.qa.text) - 1 if s.qa.text.strip().isdigit() else -1
        ok = a.qs.add(s.sp.text, s.qt.text, [f.text for f in s.qo], idx, s.qe.text); info(a.t('add_q'), a.t('saved') if ok else a.t('invalid'), a.t('ok'))
        if ok: s.refresh()
