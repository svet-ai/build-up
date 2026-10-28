[app]
title = BilimUp
package.name = bilimup
package.domain = kz.bilimup
source.dir = .
source.include_exts = py,png,jpg,json,kv,atlas
source.exclude_dirs = tests,bin
version = 0.2.0
requirements = python3==3.11.5,hostpython3==3.11.5,kivy==2.3.0,sqlite3,openssl,certifi
orientation = portrait
fullscreen = 0
android.api = 33
android.ndk = 25b
android.minapi = 24
android.permissions = INTERNET
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
p4a.branch = v2024.01.21

[buildozer]
log_level = 2
warn_on_root = 1
