@echo off
setlocal
set "ROOT=%~dp0"
rem Prefer editable/src layout; fall back to installed package on PYTHONPATH
set "PYTHONPATH=%ROOT%src;%PYTHONPATH%"
python -m talaria_cli %*
exit /b %ERRORLEVEL%
