import time
import random

def generate_noise():
    print("[*] Generating noise for stealth...")
    for _ in range(random.randint(4, 8)):
        time.sleep(random.uniform(0.15, 1.1))
    print("[*] Noise completed")