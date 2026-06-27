# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[('icone.ico', '.')],
    hiddenimports=['openai', 'PyQt6.QtWidgets', 'PyQt6.QtCore', 'PyQt6.QtGui'],
    hookspath=[],
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'numpy', 'scipy'],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GPT-Image-Generator',
    debug=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    console=False,          # pas de fenêtre console
    icon='icone.ico',
)
