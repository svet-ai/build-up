from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen
from widget_cards import _n


class Page(Screen):
    def __init__(s, **kw):
        super().__init__(**kw)
        s.app = App.get_running_app()
        sv = ScrollView(do_scroll_x=False)
        s.box = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(16),
            spacing=dp(12),
        )
        s.box.bind(minimum_height=s.box.setter('height'))
        sv.add_widget(s.box)
        s.add_widget(sv)

    def on_pre_enter(s, *a):
        s.refresh()

    def refresh(s):
        # Reset the animation stagger counter from the actual widget_cards module.
        _n[0] = 0
        s.box.clear_widgets()
        s.build_ui()

    def build_ui(s):
        pass
