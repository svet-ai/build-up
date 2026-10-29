from widget_cards import Card, lbl, btn, NEON
from screen_base import Page

class MistakesScreen(Page):
    def build_ui(s):
        a = s.app; ms = a.db.mistakes(a.user['login']); s.box.add_widget(btn(a.t('back'), lambda: a.go('subjects'), False, 40))
        s.box.add_widget(lbl(f"{a.t('mistakes')}: {len(ms)}", 22, NEON, True))
        if ms: s.box.add_widget(btn(a.t('retry'), lambda: a.quiz_with(ms[:20], a.t('mistakes'), min(len(ms), 20))))
        for q in ms:
            c = Card(); c.add_widget(lbl(f"{a.sname(q['s'])}: {q['q']}", 14)); s.box.add_widget(c)
