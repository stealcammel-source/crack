import time
import random

def simulate_injection():
    targets = ["chrome.exe", "msedge.exe", "brave.exe", "firefox.exe", "steam.exe", "discord.exe"]
    target = random.choice(targets)
    time.sleep(random.uniform(0.3, 1.4))
    return f"Simulated process injection into {target}"