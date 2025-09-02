# YukkiMusic/logging.py
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import re
from typing import Optional
from pyrogram import Client

from config import LOG_FILE_NAME

# ----- Konfigurasi logging aman -----
LOG_PATH = Path(LOG_FILE_NAME)
if LOG_PATH.parent and str(LOG_PATH.parent) not in (".", ""):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

handlers = [
    RotatingFileHandler(
        LOG_PATH, maxBytes=5_000_000, backupCount=10, encoding="utf-8", delay=True
    ),
    logging.StreamHandler(),
]

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=handlers,
    force=True,  # pastikan override konfigurasi lama
)

# Reduksi kebisingan lib
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)
logging.getLogger("pymongo").setLevel(logging.ERROR)
logging.getLogger("ntgcalls").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("telethon").setLevel(logging.ERROR)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)

# ----- Helper: resolve LOG_GROUP_ID aman dari angka/@username/link -----
def _maybe_int(s: str) -> Optional[int]:
    s = s.strip()
    if re.fullmatch(r"-?\d{5,}", s):
        try:
            return int(s)
        except ValueError:
            return None
    return None

async def resolve_log_chat_id(app: Client, value) -> int:
    """
    Terima: int | str('-100...') | '@username' | 'https://t.me/...'
    Return: chat_id (int), raise kalau tidak valid/akses ditolak.
    """
    if value is None:
        raise ValueError("LOG_GROUP_ID/LOG_GROUP belum diisi")
    if isinstance(value, int):
        await app.get_chat(value)
        return value

    s = str(value).strip()
    if s.startswith(("https://t.me/", "t.me/")):
        s = s.split("/", maxsplit=3)[-1].split("?")[0]

    as_int = _maybe_int(s)
    if as_int is not None:
        await app.get_chat(as_int)
        return as_int

    if not s.startswith("@"):
        s = "@" + s
    chat = await app.get_chat(s)
    return chat.id