@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" goto falta
".venv\Scripts\python.exe" google_login.py
if errorlevel 1 goto error
echo Ahora podes abrir 3_ABRIR_PANEL.bat.
pause
exit /b 0
:falta
echo Primero ejecuta 1_INSTALAR.bat.
pause
exit /b 1
:error
echo No se completo la conexion. Revisa el mensaje anterior.
pause
exit /b 1
