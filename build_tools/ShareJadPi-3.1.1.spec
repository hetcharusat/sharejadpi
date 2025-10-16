# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['../sharejadpi.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../templates', 'templates'),
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
    name='ShareJadPi-3.1.1',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Disabled UPX for stability
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Windowed for tray mode
    disable_windowed_traceback=True,  # Better error handling for windowed mode
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='../assets/icon.ico',  # Custom green sphere icon
    version_info=None,
)
