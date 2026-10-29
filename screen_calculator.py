from kivy.metrics import dp
from kivy.uix.gridlayout import GridLayout
from widget_cards import Card, lbl, btn, NEON
from service_calculator import calc
from screen_base import Page

KEYS = ['C', '(', ')', 'DEL', '7', '8', '9', '÷', '4', '5', '6', '×', '1', '2', '3', '-', '0', '.', '^', '+', 'sqrt(', 'sin(', 'cos(', 'tan(', 'ln(', 'log(', 'pi', '=']

class CalculatorScreen(Page):
    def build_ui(s):
        a = s.app; s.ex = ''; s.box.add_widget(btn(a.t('back'), lambda: a.go('subjects'), False, 40))
        c = Card(); s.disp = lbl('0', 30, NEON, True, halign='right'); c.add_widget(s.disp); s.box.add_widget(c)
        g = GridLayout(cols=4, spacing=dp(6), size_hint_y=None, height=dp(7 * 56))
        for k in KEYS: g.add_widget(btn(k, lambda k=k: s.press(k), k in '=C' , 50))
        s.box.add_widget(g)
    def press(s, k):
        if k == 'C': s.ex = ''
        elif k == 'DEL': s.ex = s.ex[:-1]
        elif k == '=': s.ex = calc(s.ex) if s.ex else ''
        else: s.ex = ('' if s.ex == 'Error' else s.ex) + k
        s.disp.text = s.ex or '0'
