# YukkiMusic/utils/logger.py (PATCH anti-circular)
from config import LOG_GROUP_ID
from YukkiMusic.utils.database import is_on_off

async def play_logs(message, streamtype):
    # Matikan cepat kalau fitur log off
    if not await is_on_off(2):
        return

    # Ambil client dari message (tanpa impor app global)
    app = getattr(message, "client", None) or getattr(message, "_client", None)
    if app is None:
        return  # tidak ada client, gak bisa kirim log

    # Info chat
    chatusername = f"@{getattr(message.chat, 'username', None)}" if getattr(message.chat, "username", None) else "ᴘʀɪᴠᴀᴛᴇ ɢʀᴏᴜᴘ"

    # Info user (aman kalau anonim/tidak ada username)
    u = message.from_user
    user_id = getattr(u, "id", "-")
    user_mention = u.mention if u else "-"
    user_username = f"@{u.username}" if (u and u.username) else "-"

    # Ambil query (text/caption) aman
    query = "-"
    if getattr(message, "text", None):
        parts = message.text.split(None, 1)
        if len(parts) > 1:
            query = parts[1]
    elif getattr(message, "caption", None):
        parts = message.caption.split(None, 1)
        if len(parts) > 1:
            query = parts[1]

    # Mention bot
    try:
        bot_mention = getattr(app, "mention", None)
        if not bot_mention:
            me = await app.get_me()
            bot_mention = me.mention
    except Exception:
        bot_mention = "Bot"

    logger_text = f"""
<b>{bot_mention} ᴘʟᴀʏ ʟᴏɢ</b>

<b>ᴄʜᴀᴛ ɪᴅ :</b> <code>{message.chat.id}</code>
<b>ᴄʜᴀᴛ ɴᴀᴍᴇ :</b> {message.chat.title}
<b>ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ :</b> {chatusername}

<b>ᴜsᴇʀ ɪᴅ :</b> <code>{user_id}</code>
<b>ɴᴀᴍᴇ :</b> {user_mention}
<b>ᴜsᴇʀɴᴀᴍᴇ :</b> {user_username}

<b>ǫᴜᴇʀʏ :</b> {query}
<b>sᴛʀᴇᴀᴍᴛʏᴘᴇ :</b> {streamtype}""".strip()

    # Hindari spam kalau log group-nya sama dengan chat asal
    if message.chat.id == LOG_GROUP_ID:
        return

    try:
        await app.send_message(
            chat_id=LOG_GROUP_ID,
            text=logger_text,
            disable_web_page_preview=True,
        )
    except Exception:
        # Biar gak bikin crash saat log gagal
        pass