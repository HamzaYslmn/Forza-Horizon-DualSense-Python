@echo off
REM Build a standalone single-file EXE of FH-DualSense.
REM Output: packaging\windows\dist\FH-DualSense-vX.Y.Z.exe
REM (no install, no traces - MEIPASS auto-cleans on exit)
REM Requires: uv  (https://docs.astral.sh/uv/)

setlocal EnableDelayedExpansion
pushd "%~dp0..\.."

REM MARK: read version = "X.Y.Z" from src\pyproject.toml
set "VER="
for /f "tokens=*" %%L in ('findstr /b /c:"version" src\pyproject.toml') do (
    if not defined VER (
        set "LINE=%%L"
        for /f "tokens=2 delims==" %%V in ("!LINE!") do (
            set "RAW=%%V"
            set "RAW=!RAW: =!"
            set "RAW=!RAW:"=!"
            set "VER=!RAW!"
        )
    )
)
if not defined VER (
    echo Could not read version from src\pyproject.toml
    popd
    exit /b 1
)
echo Building FH-DualSense v%VER% ...

set "DIST=%~dp0dist"
set "WORK=%~dp0build"

if exist "%WORK%" rmdir /s /q "%WORK%"
if exist "%DIST%" (
    rmdir /s /q "%DIST%" 2>nul
    if exist "%DIST%" (
        echo.
        echo ERROR: Could not clean "%DIST%" - a previous FH-DualSense.exe is probably still running.
        echo        Right-click the tray icon and choose Quit, then retry.
        popd
        exit /b 1
    )
)

uvx --from "pyinstaller>=6.11.1" --with customtkinter --with textual --with hidapi --with psutil --with dotenv --with pystray --with pillow pyinstaller "%~dp0fhds.spec" --distpath "%DIST%" --workpath "%WORK%" --noconfirm --clean
if errorlevel 1 (
    echo.
    echo Build FAILED.
    popd
    exit /b 1
)

REM MARK: rename output to include version
if exist "%DIST%\FH-DualSense.exe" (
    move /y "%DIST%\FH-DualSense.exe" "%DIST%\FH-DualSense-v%VER%.exe" >nul
)

echo.
echo Build OK. Executable: %DIST%\FH-DualSense-v%VER%.exe
popd
endlocal
