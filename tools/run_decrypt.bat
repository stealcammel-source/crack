@echo off
title STEAL(v0.2) - Decrypt Tool
echo ================================================
echo     STEAL(v0.2) — DECRYPT TOOL
echo ================================================
echo.

:: Пробуем разные возможные пути к Python 3.12
set PYTHON_PATH=C:\Users\dom\AppData\Local\Programs\Python\Python312\python.exe

if not exist "%PYTHON_PATH%" (
    echo [!] Python 3.12 не найден по стандартному пути.
    echo     Пытаемся найти python.exe...
    for %%i in (python.exe) do set PYTHON_PATH=%%~$PATH:i
)

echo Запускаем decrypt.py с помощью: %PYTHON_PATH%
echo.

"%PYTHON_PATH%" decrypt.py

echo.
echo ================================================
echo Расшифровка завершена.
echo Нажмите любую клавишу для закрытия окна...
pause >nul