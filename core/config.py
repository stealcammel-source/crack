import random
import os
import sys

CONFIG = {
    "delay_range": (0.4, 2.8),
    "exfil_url": "http://127.0.0.1:5000/upload",
    "archive_name": "loot.zip",
    "output_dir": "results",
}

def jitter():
    return random.uniform(*CONFIG["delay_range"])


def get_output_path(filename: str) -> str:
    if getattr(sys, 'frozen', False):
        root_path = os.path.dirname(sys.executable)
    else:
        root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    output_dir = os.path.join(root_path, CONFIG["output_dir"])
    os.makedirs(output_dir, exist_ok=True)
    return os.path.join(output_dir, filename)