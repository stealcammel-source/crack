@echo off
chcp 65001 >nul
echo ================================================
echo     steal(v0.2) - Автоматическая сборка
echo ================================================

echo Очистка предыдущих сборок...
rd /s /q build dist 2>nul

echo Запуск сборки...
pyinstaller steal_v0.2.spec --clean

echo.
echo ================================================
echo Копирование decrypt файлов...

if exist "run_decrypt.bat" (
    copy /Y "run_decrypt.bat" "dist\steal_v0.2\" >nul
    echo [+] run_decrypt.bat скопирован
) else (
    echo [!] run_decrypt.bat не найден в корне проекта!
)

if exist "decrypt.py" (
    copy /Y "decrypt.py" "dist\steal_v0.2\" >nul
    echo [+] decrypt.py скопирован
) else (
    echo [!] decrypt.py не найден в корне проекта!
)

echo.
echo ================================================
echo Сборка завершена!
echo .exe находится в: dist\steal_v0.2\
echo.
pause