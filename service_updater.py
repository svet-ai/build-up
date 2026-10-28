import json, urllib.request, ssl

def vt(v): return tuple(int(x) for x in str(v).split('.') if x.isdigit())

def fetch(url, timeout=8):
    """Run in a background thread. Remote JSON: {"version","apk_url","questions":[{s,q,o,a,e}]}"""
    try:
        import certifi; ctx = ssl.create_default_context(cafile=certifi.where())
    except Exception: ctx = None
    with urllib.request.urlopen(url, timeout=timeout, context=ctx) as r: return json.loads(r.read().decode('utf-8'))

def apply(d, current, qs):
    """Run on the main thread (SQLite): merge new questions, report a newer app version."""
    added = qs.merge(d.get('questions', []))
    newer = vt(d.get('version', '0')) > vt(current)
    return {'apk': d.get('apk_url') if newer else None, 'version': d.get('version'), 'added': added}
