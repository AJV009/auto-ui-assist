# -*- mode: python ; coding: utf-8 -*-

import os

# Get the absolute path to the directory containing the spec file
spec_dir = os.path.abspath(os.path.dirname(SPEC))

# Specify the path to your .env file relative to the spec file directory
env_file_path = os.path.join(spec_dir, '.env')

# Specify the paths to the directories containing dynamically imported modules
module_dirs = ['utils', 'action', 'app_tools']

a = Analysis(
    ['UI.py'],
    pathex=[],
    binaries=[],
    datas=[(env_file_path, '.'), *[(os.path.join(dir), dir) for dir in module_dirs]],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='UI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
