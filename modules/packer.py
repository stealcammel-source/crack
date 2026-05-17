import zipfile
import os

def pack(files: list, output: str = "loot.zip"):
    if not files:
        print("[!] Нет файлов для упаковки")
        return None

    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f in files:
            if os.path.exists(f):
                z.write(f, arcname=os.path.basename(f))
    print(f"[*] Упаковано {len(files)} файлов → {output}")
    return output