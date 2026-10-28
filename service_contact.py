from urllib.parse import quote
NUMBERS = ('+77074548249', '+77077153750')

def pretty(n): return f'{n[:2]} {n[2:5]} {n[5:8]} {n[8:]}'
def wa_url(number, text): return 'https://wa.me/' + number.lstrip('+') + '?text=' + quote(text)

def open_url(url):
    """Android: open through an Intent (WhatsApp if installed, otherwise the browser)."""
    try:
        from kivy.utils import platform
        if platform == 'android':
            from jnius import autoclass
            Intent, Uri = autoclass('android.content.Intent'), autoclass('android.net.Uri')
            autoclass('org.kivy.android.PythonActivity').mActivity.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url))); return True
    except Exception: pass
    import webbrowser; return webbrowser.open(url)
