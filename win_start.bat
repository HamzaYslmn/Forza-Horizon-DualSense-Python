@echo off
REM FH DualSense — Windows launcher. Downloads the latest release into ./app and runs it.

setlocal enabledelayedexpansion
set "REPO=HamzaYslmn/Forza-Horizon-DualSense-Python"
set "RELEASES=https://github.com/%REPO%/releases/latest"
set "APP=%~dp0app"
set "PYPROJECT=%APP%\src\pyproject.toml"
set "GAME_CMD=%*"

set "IS_ADMIN=0"
net session >nul 2>&1 && set "IS_ADMIN=1"
if "%IS_ADMIN%"=="1" (echo Running as administrator.) else (echo Running as standard user.)

echo Checking latest release...
for /f "usebackq delims=" %%v in (`powershell -NoProfile -Command "try { (Invoke-RestMethod -UseBasicParsing 'https://api.github.com/repos/%REPO%/releases/latest' -Headers @{'User-Agent'='fhds'}).tag_name } catch { '' }"`) do set "LATEST=%%v"
set "SOURCE=tags"
if "!LATEST!"=="" (
    echo No release found. Using 'main' branch.
    set "LATEST=main"
    set "SOURCE=heads"
)

set "CURRENT="
if exist "%PYPROJECT%" (
    for /f "tokens=1* delims==" %%a in ('findstr /b /r /c:"^version" "%PYPROJECT%"') do (
        if not defined CURRENT (
            set "v=%%b"
            set "v=!v: =!"
            set "v=!v:"=!"
            set "CURRENT=v!v!"
        )
    )
)

if "!SOURCE!"=="heads" (echo Refreshing 'main' branch ^(installed: !CURRENT!^)... & goto :install)
if not defined CURRENT (echo Installing !LATEST!... & goto :install)
if "!CURRENT!"=="!LATEST!" (echo Up to date ^(!CURRENT!^). & goto :run)
echo Update available: !CURRENT! -^> !LATEST!
echo If the automatic update doesn't work, download manually start script from:
echo   %RELEASES%
set /p "ans=Update now? [Y/n]: "
if /I "!ans!"=="n" goto :run

:install
set "ZIP=%~dp0fhds.zip"
set "EXTRACT=%~dp0_extract"
echo Downloading !LATEST!...
powershell -NoProfile -Command "$ProgressPreference='SilentlyContinue'; try { Invoke-WebRequest -UseBasicParsing 'https://github.com/%REPO%/archive/refs/!SOURCE!/!LATEST!.zip' -OutFile '%ZIP%'; if (Test-Path '%EXTRACT%') { Remove-Item -Recurse -Force '%EXTRACT%' }; Expand-Archive -LiteralPath '%ZIP%' -DestinationPath '%EXTRACT%' -Force } catch { exit 1 }"
if errorlevel 1 (
    echo.
    echo Download or extract failed. Download the latest release manually from:
    echo   %RELEASES%
    echo and extract its contents into the "app" folder next to this script.
    echo.
    if not exist "%APP%\src\main.py" (pause & exit /b 1)
    goto :run
)
if exist "%APP%" rmdir /s /q "%APP%"
for /d %%d in ("%EXTRACT%\*") do move "%%d" "%APP%" >nul
rmdir /s /q "%EXTRACT%"
del "%ZIP%"
echo Installed !LATEST!.

:run
where uv >nul 2>nul || (
    echo uv was not found. Installing from https://astral.sh/uv/ ...
    powershell -NoProfile -Command "irm https://astral.sh/uv/install.ps1 | iex"
    where uv >nul 2>nul || (echo uv installed but not on PATH. Restart your terminal. & pause & exit /b 1)
)

cd /d "%APP%\src"
if defined GAME_CMD (echo Launching game: !GAME_CMD! & start "" !GAME_CMD!)
set "PYTHONHOME="
set "PYTHONPATH="
set "PYTHONNOUSERSITE=1"
set "FHDS_IS_ADMIN=%IS_ADMIN%"
uv run main.py
echo.
echo App exited with code %ERRORLEVEL%.
if not defined GAME_CMD pause >nul
endlocal
