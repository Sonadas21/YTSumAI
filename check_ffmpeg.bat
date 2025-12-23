@echo off
echo ============================================================
echo FFmpeg Path Refresh Script
echo ============================================================
echo.
echo This script will:
echo 1. Find FFmpeg installation location
echo 2. Test if FFmpeg is accessible
echo.

rem Common FFmpeg locations
set "FFMPEG_PATHS=C:\ffmpeg\bin;C:\Program Files\ffmpeg\bin;%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin"

echo Searching for FFmpeg...
echo.

rem Check if ffmpeg is already in PATH
where ffmpeg >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] FFmpeg found in PATH!
    ffmpeg -version | findstr "ffmpeg version"
    echo.
    echo You can now restart your Streamlit app.
    pause
    exit /b 0
)

echo FFmpeg not in current PATH. Searching common locations...
echo.

rem Try to find FFmpeg
for %%p in ("%FFMPEG_PATHS:;=" "%") do (
    if exist "%%~p\ffmpeg.exe" (
        echo [FOUND] FFmpeg at: %%~p
        echo.
        echo Testing FFmpeg...
        "%%~p\ffmpeg.exe" -version | findstr "ffmpeg version"
        echo.
        echo ============================================================
        echo SOLUTION: Add this to your PATH:
        echo %%~p
        echo.
        echo Then RESTART VS Code / Terminal completely
        echo ============================================================
        pause
        exit /b 0
    )
)

echo [NOT FOUND] Could not locate FFmpeg automatically.
echo.
echo Please check:
echo 1. Run: winget list ffmpeg
echo 2. Find installation directory
echo 3. Add bin folder to PATH
echo 4. Restart terminal
echo.
pause
