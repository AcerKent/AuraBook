@echo off
REM Automated Execution Script
REM usage: run_auto.bat

REM Activate environment and run script
REM Activate environment and run script
"D:\Company\Projects\CondaEnvs\ebook\python.exe" "%~dp0main.py"

REM Optional: Auto-close if successful, pause on error
if %errorlevel% neq 0 pause
