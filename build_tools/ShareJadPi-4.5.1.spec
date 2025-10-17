# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['../sharejadpi.py'],
    pathex=[],
    binaries=[
        ('../cloudflared.exe', '.'),
    ],
    datas=[
        ('../templates', 'templates'),
        ('../static', 'static'),
        ('../assets/icon.ico', 'assets'),
    ],
    hiddenimports=[
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
    ],
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
    [],
    name='ShareJadPi-4.5.1',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='../assets/icon.ico',
    version_info=None,
)
