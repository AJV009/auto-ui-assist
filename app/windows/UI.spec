# -*- mode: python ; coding: utf-8 -*-

# PyInstaller Spec File for Auto UI Assist
# This file contains specifications for creating an executable using PyInstaller.

import os

# 1. Path Setup
# Get the absolute path to the directory containing the spec file
spec_dir = os.path.abspath(os.path.dirname(SPEC))

# 2. Module Directories
# Specify the paths to the directories containing dynamically imported modules
module_dirs = ['utils', 'action', 'app_tools']

# 3. Analysis Configuration
# Define the Analysis object, which collects all the necessary files for the application
a = Analysis(
    ['UI.py'],  # The main script of your application
    pathex=[],  # Additional paths to search for imports (empty in this case)
    binaries=[],  # Any additional binary files (empty in this case)
    datas=[*[(os.path.join(dir), dir) for dir in module_dirs]],  # Include all files from module_dirs
    hiddenimports=['comtypes','comtypes.stream'],  # Explicitly include these modules
    hookspath=[],  # Custom hook scripts (empty in this case)
    hooksconfig={},  # Configuration for hooks (empty in this case)
    runtime_hooks=[],  # Scripts to run at runtime (empty in this case)
    excludes=[],  # Modules to exclude (empty in this case)
    noarchive=False,  # If True, don't place Python bytecode in an archive
    optimize=2,  # Level of bytecode optimization (0-2)
)

# 4. Create the Executable
# PYZ creates a .pyz archive of the Python bytecode
pyz = PYZ(a.pure)

# EXE defines the final executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],  # Additional files to include (empty in this case)
    name='UI',  # Name of the output executable
    debug=False,  # If True, creates a debug executable
    bootloader_ignore_signals=False,  # If True, bootloader ignores signals
    strip=False,  # If True, strips symbols from the executable
    upx=True,  # If True, compresses the executable using UPX
    upx_exclude=[],  # Files to exclude from UPX compression
    runtime_tmpdir=None,  # Temporary directory for extracting libraries
    console=True,  # If True, opens a console window
    disable_windowed_traceback=False,  # If True, disables traceback dump on unhandled exception
    argv_emulation=False,  # If True, enables argv emulation for macOS
    target_arch=None,  # Target architecture (None means auto-detect)
    codesign_identity=None,  # Code signing identity (for macOS)
    entitlements_file=None,  # Entitlements file (for macOS)
    onefile=True  # If True, creates a single file executable
)

# Detailed Explanation:
# 1. The spec file starts by importing the 'os' module for file path operations.
# 
# 2. It gets the absolute path of the directory containing the spec file using os.path.abspath().
# 
# 3. module_dirs lists the directories containing modules that need to be included in the executable.
# 
# 4. The Analysis object collects all necessary files:
#    - 'UI.py' is the main script of the application.
#    - datas includes all files from the specified module directories.
#    - hiddenimports explicitly includes 'comtypes' and 'comtypes.stream' modules.
# 
# 5. PYZ creates a Python archive of the collected modules.
# 
# 6. EXE creates the final executable:
#    - It includes all collected scripts, binaries, and data.
#    - 'name' sets the output executable name to 'UI'.
#    - 'console=True' means it will open a console window when run.
#    - 'onefile=True' creates a single file executable instead of a directory.
# 
# This spec file ensures that all necessary modules and data files are included in the final executable,
# making it possible to run the Auto UI Assist application on systems without Python installed.
