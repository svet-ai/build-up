from widget_cards import lbl, btn, NEON
from .base import Page

class GradeScreen(Page):
    def build_ui(s):
        a = s.app; s.box.add_widget(lbl(a.t('pick_grade'), 24, NEON, True))
        for g in ['5', '6', '7', '8', '9', '10', '11', 'ent']:
            s.box.add_widget(btn(a.t('ent') if g == 'ent' else (g + a.t('grade_n')), lambda g=g: s.pick(g), g == 'ent'))
    def pick(s, g):
        s.app.auth.update(s.app.user['login'], grade=g); s.app.user['grade'] = g; s.app.go('home')
