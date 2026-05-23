# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for Forza-Horizon-DualSense.

One-file, windowed (no console). On launch the bootloader extracts everything
into %TEMP%\\_MEIxxxxxx (MEIPASS) and auto-deletes it on exit. Recent PyInstaller
versions also handle WM_QUERYENDSESSION so cleanup runs on Windows shutdown.

Build:
    packaging\\windows\\build_exe.bat
"""

from pathlib import Path
import re
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

SRC = Path(SPECPATH).resolve().parents[1] / "src"
ICON = SRC / "data" / "icon.ico"

# MARK: read version from pyproject.toml and emit a Windows VERSIONINFO file
def _read_version() -> str:
    py = (SRC / "pyproject.toml").read_text(encoding="utf-8")
    m = re.search(r'^version\s*=\s*"([^"]+)"', py, re.M)
    return m.group(1) if m else "0.0.0"

def _version_tuple(v: str) -> tuple:
    parts = [int(x) for x in re.findall(r"\d+", v)[:4]]
    while len(parts) < 4:
        parts.append(0)
    return tuple(parts)

VERSION = _read_version()
VTUP = _version_tuple(VERSION)
VERSION_FILE = Path(SPECPATH) / "version_info.txt"
VERSION_FILE.write_text(f"""# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers={VTUP},
    prodvers={VTUP},
    mask=0x3f, flags=0x0, OS=0x40004, fileType=0x1, subtype=0x0, date=(0, 0),
  ),
  kids=[
    StringFileInfo([
      StringTable('040904B0', [
        StringStruct('CompanyName', 'HamzaYslmn'),
        StringStruct('FileDescription', 'Forza Horizon DualSense adaptive triggers'),
        StringStruct('FileVersion', '{VERSION}'),
        StringStruct('InternalName', 'FH-DualSense'),
        StringStruct('LegalCopyright', 'MIT License'),
        StringStruct('OriginalFilename', 'FH-DualSense.exe'),
        StringStruct('ProductName', 'FH DualSense'),
        StringStruct('ProductVersion', '{VERSION}'),
      ])
    ]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
""", encoding="utf-8")

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
    icon=str(ICON),
    version=str(VERSION_FILE),
)
