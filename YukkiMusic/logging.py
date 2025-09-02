import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config import LOG_FILE_NAME

# Tentukan path file log (boleh nama file saja, atau "logs/nama.log")
LOG_PATH = Path(LOG_FILE_NAME)

# Buat folder kalau ada parent directory (mis. "logs/kenlogs.txt")
if LOG_PATH.parent and str(LOG_PATH.parent) not in (".", ""):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

# Siapkan handlers (file + console)
handlers = [
    RotatingFileHandler(
        LOG_PATH,
        maxBytes=5_000_000,
        backupCount=10,
        encoding="utf-8",   # penting biar aman karakter non-ASCII
        delay=True,         # file dibuka saat dipakai pertama kali
    ),
    logging.StreamHandler(),
]

# Paksa konfigurasi agar tidak diabaikan kalau sudah ada konfigurasi sebelumnya
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=handlers,
    force=True,  # Python 3.8+ : override konfigurasi sebelumnya
)

# Kurangi kebisingan lib pihak ketiga
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)
logging.getLogger("pymongo").setLevel(logging.ERROR)
logging.getLogger("ntgcalls").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("telethon").setLevel(logging.ERROR)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)