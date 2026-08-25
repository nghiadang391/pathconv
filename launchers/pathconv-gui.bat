@echo off
rem One-click launcher for the pathconv GUI on Windows.
rem Requires pathconv to be installed first (pipx install / pip install .),
rem which puts the `pathconv` GUI command on your PATH. The gui-scripts entry
rem point opens with no console window.
where pathconv >nul 2>nul
if errorlevel 1 (
    echo pathconv is not installed. Install it first, e.g.:
    echo     pipx install git+https://github.com/nghiadang391/pathconv.git
    pause
    exit /b 1
)
start "" pathconv %*
