@echo off
setlocal
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" goto instalar
py -m venv .venv
if errorlevel 1 goto error
:instalar
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto error
echo Instalacion terminada. Ahora abri 2_CONECTAR_GOOGLE.bat.
pause
exit /b 0
:error
echo No se completo la instalacion. Copia el error de esta ventana.
pause
exit /b 1
