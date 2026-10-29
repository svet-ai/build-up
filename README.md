# BilimUp (Kivy / Buildozer)
Run: `pip install -r requirements.txt && python main.py`. Tests: `python -m unittest discover tests`.
APK: `buildozer android debug` or the GitHub Actions workflow.
First launch creates `admin` with a random password shown once (not stored in source). Users are created only by the admin.
Data is a local SQLite DB (not synced between devices); a server backend is the next step for sync and a global leaderboard.
Not done yet: calculator, periodic table, formulas, large question base (3000 questions across 16 subjects; admins can add more), grade/ENT subject filter, creative-exam tracks.

## v0.2: calculator (safe AST evaluator), 118-element periodic table, formulas, mistakes collection, auto-update
Auto-update: set `update_url` in `assets/config.json` to a JSON file you host: `{"version":"0.3.0","apk_url":"https://.../BilimUp.apk","questions":[{"s":"math","q":"...","o":["a","b","c","d"],"a":0,"e":"..."}]}`.
On start (and from Profile) the app merges new questions (no duplicates) and offers the APK link if the version is newer. Android installs the APK only after user confirmation.
