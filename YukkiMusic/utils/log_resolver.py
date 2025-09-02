import re
from typing import Union, Optional
from pyrogram import Client

def _maybe_int(s: str) -> Optional[int]:
    s = s.strip()
    if re.fullmatch(r"-?\d{5,}", s):
        try:
            return int(s)
        except ValueError:
            return None
    return None

async def resolve_log_chat_id(app: Client, value: Union[int, str, None]) -> int:
    if value is None:
        raise ValueError("LOG_GROUP_ID/LOG_GROUP belum diisi")
    if isinstance(value, int):
        await app.get_chat(value)  # validasi akses
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