# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
    ('../assets/icon.ico', 'assets'),
    ('../static', 'static'),
    ('../templates', 'templates'),
    ('../cloudflared.exe', '.'),
]

hidden_imports = [
    'qrcode', 'PIL', 'pystray', 'flask', 'winotify'
]

a = Analysis(
    ['../sharejadpi.py'],
    pathex=[],
    binaries=[],
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
    name='ShareJadPi-4.5.4',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='../assets/icon.ico',
)
