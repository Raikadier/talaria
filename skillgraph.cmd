@echo off
REM SkillGraph CLI launcher (dev-friendly without requiring pip install)
set "ROOT=%~dp0"
set "PYTHONPATH=%ROOT%;%PYTHONPATH%"
"C:\Users\david\AppData\Local\Python\bin\python.exe" -m skillgraph_cli %*
