# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for Forza-Horizon-DualSense (Linux).

One-file ELF binary. On launch the bootloader extracts everything into a
temp dir (MEIPASS) and auto-deletes it on exit. No Windows VERSIONINFO and
no embedded icon (PyInstaller can't embed an icon into a bare ELF).

Build:
    packaging/linux/build_elf.sh
"""

from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

SRC = Path(SPECPATH).resolve().parents[1] / "src"

datas = [
    (str(SRC / "data" / "icon.ico"), "data"),
    (str(SRC / "data" / "icon.png"), "data"),
    (str(SRC / "pyproject.toml"), "."),
    (str(SRC / "lang"), "lang"),
]
datas += collect_data_files("customtkinter")
datas += collect_data_files("textual")

hiddenimports = []
hiddenimports += collect_submodules("textual")
hiddenimports += collect_submodules("customtkinter")
hiddenimports += collect_submodules("pystray")
hiddenimports += ["PIL.Image", "PIL.ImageDraw"]

a = Analysis(
    [str(SRC / "main.py")],
    pathex=[str(SRC)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="FH-DualSense",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
