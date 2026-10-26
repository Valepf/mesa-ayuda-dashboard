@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" goto falta
".venv\Scripts\python.exe" -m streamlit run app.py
if errorlevel 1 pause
exit /b
:falta
echo Primero ejecuta 1_INSTALAR.bat.
pause
exit /b 1
