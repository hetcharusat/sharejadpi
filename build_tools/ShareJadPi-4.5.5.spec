# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
    ('../assets/icon.ico', 'assets'),
    ('../static', 'static'),
    ('../templates', 'templates'),
]

hidden_imports = [
    'qrcode',
    'qrcode.image.pil',
    'PIL',
    'PIL.Image',
    'PIL.ImageDraw',
    'PIL.ImageFont',
    'pystray',
    'pystray._win32',
    'flask',
    'werkzeug',
    'jinja2',
    'click',
    'itsdangerous',
    'markupsafe',
    'requests',
    'winotify',
]

a = Analysis(
    ['../sharejadpi.py'],
    pathex=[],
    binaries=[('../cloudflared.exe', '.')],
    datas=added_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='ShareJadPi-4.5.5',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    icon='../assets/icon.ico',
)
