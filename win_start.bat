@echo off
REM FH5 DualSense — Windows stub launcher.
REM Downloads the latest GitHub release into ./app and runs it.
REM Asks before updating to a newer version.

setlocal enabledelayedexpansion
set "REPO=HamzaYslmn/Forza-Horizon-DualSense-Python"
set "ROOT=%~dp0"
set "APP=%ROOT%app"
set "VERSION_FILE=%APP%\.version"

REM --- Launcher self-version. Bump this when win_start.bat changes. ---
set "LAUNCHER_VERSION=2"

REM --- Check if this launcher script itself is out of date ---
set "REMOTE_LAUNCHER="
for /f "usebackq delims=" %%r in (`powershell -NoProfile -ExecutionPolicy Bypass -Command "try { $t = (Invoke-WebRequest -UseBasicParsing -Uri 'https://raw.githubusercontent.com/%REPO%/main/win_start.bat' -Headers @{'User-Agent'='fh5ds-launcher'}).Content; if ($t -match 'LAUNCHER_VERSION=(\d+)') { $Matches[1] } } catch { '' }"`) do set "REMOTE_LAUNCHER=%%r"

if not "!REMOTE_LAUNCHER!"=="" if not "!REMOTE_LAUNCHER!"=="!LAUNCHER_VERSION!" (
    echo.
    echo ============================================================
    echo  A newer win_start.bat is available ^(yours: !LAUNCHER_VERSION!, latest: !REMOTE_LAUNCHER!^).
    echo  The auto-updater can refresh the app, but it cannot replace
    echo  this launcher script itself. Please download the new one:
    echo.
    echo    https://github.com/%REPO%/releases/latest
    echo.
    echo  Opening the releases page in your browser...
    echo ============================================================
    start "" "https://github.com/%REPO%/releases/latest"
    echo.
    pause
    exit /b 0
)

REM --- Capture trailing args (Steam %command%) so they survive later parsing ---
set "GAME_CMD=%*"

REM --- Resolve latest release tag ---
echo Checking latest release...
for /f "usebackq delims=" %%v in (`powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "try { (Invoke-RestMethod -UseBasicParsing -Uri 'https://api.github.com/repos/%REPO%/releases/latest' -Headers @{ 'User-Agent'='fh5ds-launcher' }).tag_name } catch { '' }"`) do set "LATEST=%%v"

set "SOURCE=release"
if "!LATEST!"=="" (
    echo No release found. Falling back to latest 'main' branch.
    set "LATEST=main"
    set "SOURCE=branch"
)

set "CURRENT="
if exist "%VERSION_FILE%" (
    for /f "usebackq delims=" %%c in ("%VERSION_FILE%") do set "CURRENT=%%c"
)

if "!CURRENT!"=="!LATEST!" if "!SOURCE!"=="release" (
    echo Up to date ^(!CURRENT!^).
    goto :run
)

if "!CURRENT!"=="" (
    echo Installing !LATEST!...
    goto :install
)

if "!SOURCE!"=="branch" (
    echo Refreshing 'main' branch ^(installed: !CURRENT!^)...
    goto :install
)

echo Update available: !CURRENT! -^> !LATEST!
set /p "ans=Update now? [Y/n]: "
if /I "!ans!"=="n" goto :run

:install
set "ZIP=%ROOT%fh5ds-!LATEST!.zip"
set "EXTRACT=%ROOT%_extract"
if "!SOURCE!"=="branch" (
    set "DLURL=https://github.com/%REPO%/archive/refs/heads/!LATEST!.zip"
) else (
    set "DLURL=https://github.com/%REPO%/archive/refs/tags/!LATEST!.zip"
)
echo Downloading !LATEST!...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$ProgressPreference='SilentlyContinue'; Invoke-WebRequest -UseBasicParsing -Uri '!DLURL!' -OutFile '%ZIP%'"
if errorlevel 1 (
    echo Download failed.
    if not exist "%APP%\src\main.py" (pause & exit /b 1)
    goto :run
)

if exist "%EXTRACT%" rmdir /s /q "%EXTRACT%"
echo Extracting...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "Expand-Archive -LiteralPath '%ZIP%' -DestinationPath '%EXTRACT%' -Force"

REM Move extracted top-level folder to ./app
if exist "%APP%" rmdir /s /q "%APP%"
for /d %%d in ("%EXTRACT%\*") do (
    move "%%d" "%APP%" >nul
    goto :moved
)
:moved
rmdir /s /q "%EXTRACT%"
del "%ZIP%"
> "%VERSION_FILE%" echo !LATEST!
echo Installed !LATEST!.

:run
REM --- Ensure uv is available ---
where uv >nul 2>nul
if errorlevel 1 (
    echo uv was not found.
    set /p "uvans=Install uv from https://astral.sh/uv/ now? [Y/n]: "
    if /I "!uvans!"=="n" (
        python -m pip install --user uv
    ) else (
        powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex"
    )
    where uv >nul 2>nul
    if errorlevel 1 (
        echo uv installed but not on PATH. Restart your terminal.
        pause
        exit /b 1
    )
)

REM --- Launch ---
cd /d "%APP%\src"
if defined GAME_CMD (
    echo Launching game: !GAME_CMD!
    start "" !GAME_CMD!
)
REM Isolate from any system Python (avoids pythonXY.dll mismatches).
set "PYTHONHOME="
set "PYTHONPATH="
set "PYTHONNOUSERSITE=1"
uv run main.py
set "EXITCODE=%ERRORLEVEL%"
echo.
echo App exited with code %EXITCODE%.
if not defined GAME_CMD (
    echo Press Enter to close this window...
    pause >nul
)
endlocal
