import json, os, threading, traceback, webbrowser
from kivy.base import ExceptionHandler, ExceptionManager
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from service_database import DB
from service_auth import Auth
from service_question_service import QuestionService
import service_updater as updater
from widget_bottom_navigation import BottomNav, ITEMS
from widget_cards import BG, info, gradient_bg
from screen_login import LoginScreen
from screen_grade import GradeScreen
from screen_home import HomeScreen
from screen_subjects import SubjectsScreen
from screen_test_hub import TestHub
from screen_quiz import QuizScreen
from screen_progress import ProgressScreen
from screen_profile import ProfileScreen
from screen_admin import AdminScreen
from screen_calculator import CalculatorScreen
from screen_periodic_table import PeriodicScreen
from screen_formulas import FormulasScreen
from screen_mistakes import MistakesScreen

BASE = os.path.dirname(os.path.abspath(__file__))
LANGS = ('kk', 'ru', 'en')

def load(n):
    with open(os.path.join(BASE, n), encoding='utf-8') as f: return json.load(f)

def error_view(tb):
    sv = ScrollView(); l = Label(text=tb, size_hint_y=None, font_size=dp(11), halign='left', valign='top', color=(1, .6, .6, 1))
    l.bind(width=lambda i, w: setattr(i, 'text_size', (w, None)), texture_size=lambda i, t: setattr(i, 'height', t[1])); sv.add_widget(l); return sv

class ShowErrors(ExceptionHandler):
    """Runtime errors are shown on screen instead of silently closing the app."""
    def handle_exception(s, inst):
        tb = ''.join(traceback.format_exception(type(inst), inst, inst.__traceback__))
        Clock.schedule_once(lambda dt: Popup(title='Error (send a screenshot)', content=error_view(tb), size_hint=(.96, .9)).open()); return ExceptionManager.PASS

ExceptionManager.add_handler(ShowErrors())

class BilimUp(App):
    title = 'BilimUp'
    def build(s):
        try: return s._build()
        except Exception: return error_view(traceback.format_exc())
    def _build(s):
        Window.clearcolor = BG
        s.pwfile = os.path.join(s.user_data_dir, 'admin_first_password.txt')
        s.db = DB(); s.auth = Auth(s.db); s.qs = QuestionService(BASE, s.db)
        s.tr, s.subjects, s.dirs = load('translations.json'), load('subjects.json'), load('directions.json')
        s.cfg = load('config.json'); s.user, s.lang = None, 'kk'
        root = BoxLayout(orientation='vertical'); gradient_bg(root); s.sm = ScreenManager(transition=SlideTransition(duration=.25))
        for sid, cls in (('login', LoginScreen), ('grade', GradeScreen), ('home', HomeScreen), ('subjects', SubjectsScreen), ('test', TestHub),
                         ('quiz', QuizScreen), ('progress', ProgressScreen), ('profile', ProfileScreen), ('admin', AdminScreen),
                         ('calc', CalculatorScreen), ('periodic', PeriodicScreen), ('formulas', FormulasScreen), ('mistakes', MistakesScreen)):
            s.sm.add_widget(cls(name=sid))
        s.nav = BottomNav(s); root.add_widget(s.sm); root.add_widget(s.nav); s.nav.show(False)
        pw = s.auth.first_run_password()
        if pw: open(s.pwfile, 'w').write(pw)
        elif os.path.exists(s.pwfile): os.remove(s.pwfile)
        s.sm.get_screen('login').refresh()
        # Restore the previous session after app restarts; explicit logout clears it.
        remembered = s.db.remembered_login()
        restored = s.db.user_by_login(remembered) if remembered else None
        if restored:
            Clock.schedule_once(lambda dt, u=restored: s.login(u), .15)
        Clock.schedule_once(lambda dt: s.check_updates(), 3)
        return root

    def t(s, k): return s.tr.get(k, [k] * 3)[LANGS.index(s.lang)]
    def sname(s, sid):
        for x in s.subjects:
            if x[0] == sid: return x[1 + LANGS.index(s.lang)]
        return sid
    def go(s, name):
        s.sm.current = name; s.nav.show(name in ITEMS); s.nav.set_active(name)
    def login(s, user):
        if user['role'] == 'admin':
            s.auth.mark_admin_seen()
            if os.path.exists(s.pwfile): os.remove(s.pwfile)
        s.user = user; s.db.set_session(user['login']); s.lang = user['lang'] if user['lang'] in LANGS else s.lang; s.nav.retext(); s.go('home' if user['grade'] else 'grade')
    def check_updates(s, manual=False):
        url = s.cfg.get('update_url', '')
        if not url:
            if manual: info(s.t('check_update'), s.t('no_url'), s.t('ok'))
            return
        def work():
            d, err = None, ''
            try: d = updater.fetch(url)
            except Exception as e: err = f'{type(e).__name__}: {e}'
            Clock.schedule_once(lambda dt: s.on_update(d, manual, err))
        threading.Thread(target=work, daemon=True).start()
    def on_update(s, d, manual, err=''):
        if d is None:
            if manual: info(s.t('check_update'), f"{s.t('update_fail')}\n{err[:160]}", s.t('ok'))
            return
        r = updater.apply(d, s.cfg['version'], s.qs)
        if r['apk']: info(s.t('check_update'), f"{s.t('update_avail')} {r['version']}", s.t('download'), lambda: webbrowser.open(r['apk']))
        elif r['added']: info(s.t('check_update'), f"{s.t('new_q')}: {r['added']}", s.t('ok'))
        elif manual: info(s.t('check_update'), s.t('update_none'), s.t('ok'))
    def logout(s): s.db.set_session(None); s.user = None; s.go('login')
    def set_lang(s, l):
        s.lang = l; s.nav.retext()
        if s.user: s.auth.update(s.user['login'], lang=l); s.user['lang'] = l
        s.sm.get_screen(s.sm.current).refresh()
    def quiz_with(s, qs, title, minutes):
        s.sm.get_screen('quiz').start(qs, title, minutes); s.sm.current = 'quiz'; s.sm.get_screen('quiz').refresh(); s.nav.show(False)
    def start_quiz(s, sids, title, n, minutes=None):
        s.quiz_with(s.qs.mix(sids, n), title, minutes or max(1, n))

if __name__ == '__main__':
    BilimUp().run()
