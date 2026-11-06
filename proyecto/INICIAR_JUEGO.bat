@echo off
cd /d "%~dp0"
py main.py
if errorlevel 1 (
    echo.
    echo No se pudo iniciar el juego. Instala las dependencias con:
    echo py -m pip install -r requirements.txt
    echo y ejecuta de nuevo INICIAR_JUEGO.bat
    pause
)
