import os
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from widget_cards import Card, badge, chip, lbl, btn, row, NEON, BAD, GOLD, DIM, PRI
import service_contact as contact
from screen_base import Page

def field(hint, pw=False):
    return TextInput(hint_text=hint, password=pw, multiline=False, size_hint_y=None, height=dp(48), write_tab=False,
                     background_color=(.1, .1, .27, 1), foreground_color=(1, 1, 1, 1), hint_text_color=(.6, .62, .8, 1), cursor_color=NEON, padding=[dp(14), dp(14)])

class LoginScreen(Page):
    def build_ui(s):
        a = s.app; W = (1, 1, 1, 1)
        hero = Card(hero=True); hero.add_widget(row(badge('B', W, 40), lbl('BilimUp', 24, W, True), h=44))
        cr = BoxLayout(size_hint_y=None, height=dp(38), spacing=dp(8))
        for c in (chip(a.t('ent')), chip(a.t('n_subj')), chip(a.t('rating'))): cr.add_widget(c)
        cr.add_widget(BoxLayout()); hero.add_widget(cr); hero.add_widget(lbl(a.t('hero_title'), 25, W, True)); hero.add_widget(lbl(a.t('hero_sub'), 14, (.9, .92, 1, 1))); s.box.add_widget(hero)
        if os.path.exists(a.pwfile):
            c = Card(acc=GOLD); c.add_widget(lbl('Admin', 13, DIM)); c.add_widget(lbl(f"{a.t('login')}: admin\n{a.t('password')}: {open(a.pwfile).read().strip()}", 17, GOLD, True)); s.box.add_widget(c)
        c = Card(); s.u, s.p = field(a.t('login')), field(a.t('password'), True); s.msg = lbl('', 13, BAD)
        c.add_widget(lbl(a.t('login_title'), 22, W, True))
        for w in (s.u, s.p, btn(a.t('enter'), s.go), s.msg, lbl(a.t('reg_text'), 14, DIM)): c.add_widget(w)
        for n in contact.NUMBERS: c.add_widget(btn(f"{a.t('reg_btn')}  {contact.pretty(n)}", lambda n=n: s.reg(n), False, 50))
        s.box.add_widget(c)
        s.box.add_widget(row(*[btn(n, lambda l=l: a.set_lang(l), a.lang == l, 40) for l, n in (('kk', 'Қазақша'), ('ru', 'Русский'), ('en', 'English'))], h=40))
    def reg(s, n): contact.open_url(contact.wa_url(n, s.app.t('reg_msg')))
    def go(s):
        user, st = s.app.auth.login(s.u.text, s.p.text)
        if user: s.app.login(user)
        else: s.msg.text = s.app.t('bad' if st == 'bad' else 'blocked')
