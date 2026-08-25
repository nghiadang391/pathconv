@echo off
REM Double-click launcher for the pathconv GUI on Windows.
REM Prefers the installed console script; falls back to running the module.
where pathconv-gui >nul 2>nul
if %errorlevel%==0 (
    start "" pathconv-gui
) else (
    start "" pythonw -m pathconv.gui
)
