@echo off
title Preparar y Ejecutar - Sistema de Eventos

echo =======================================================
echo     SISTEMA DE EVENTOS TI3032 - PANEL DE CONTROL
echo =======================================================
echo.

:: 1. VERIFICAR PYTHON
echo [1/3] Verificando que Python este instalado...
python --version
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Python no esta instalado o no esta configurado en el PATH.
    echo Por favor, instala Python desde python.org y marca la casilla "Add to PATH".
    pause
    exit
)
echo.

:: 2. INSTALAR LIBRERIAS
echo [2/3] Instalando librerias necesarias (Flask y PyMongo)...
pip install flask pymongo
echo.

:: 3. EJECUCION
echo [3/3] Todo listo para iniciar el servidor web.
echo.
echo.
pause

echo Iniciando servidor local...
python app.py

pause