from widget_cards import Card, lbl, btn, NEON
from screen_base import Page

class TestHub(Page):
    def build_ui(s):
        a = s.app; s.box.add_widget(lbl(a.t('test'), 26, NEON, True))
        s.box.add_widget(btn(a.t('quick'), lambda: a.start_quiz(None, a.t('quick'), 10)))
        s.box.add_widget(btn(a.t('mock'), lambda: a.start_quiz(None, a.t('mock'), 40, 40)))
        s.box.add_widget(lbl(a.t('by_subject'), 18, NEON, True))
        for sub in a.subjects:
            if a.qs.count(sub[0]): s.box.add_widget(btn(a.sname(sub[0]), lambda i=sub[0]: a.start_quiz([i], a.sname(i), 10), False, 42))
