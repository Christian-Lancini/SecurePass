[app]
title = SecurePass
package.name = securepass
package.domain = org.securepass
source.dir = .
source.include_exts = py,png,jpg,kv,txt,json,ttf
source.include_patterns = lib/*,password/*,ui/*,utils/*
version = 0.1
requirements = python3,kivy,cryptography
icon.filename = icon.png
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 0

[android]
android.api = 33
android.minapi = 21
android.sdk_path = ~/.buildozer/android/platform/android-sdk
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
