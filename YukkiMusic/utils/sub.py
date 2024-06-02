from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from YukkiMusic import app
import config


async def subcribe(client, message):
    if not config.MUST_JOIN:
        return

    try:
        await app.get_chat_member(config.MUST_JOIN, message.from_user.id)
    except UserNotParticipant:
        try:
            link = f"t.me/{config.MUST_JOIN}"
            await message.reply(
                f"**Hay kak {message.from_user.mention}, ʜᴀʀᴀᴘ ɢᴀʙᴜɴɢ ᴅᴜʟᴜ ʙɪᴀʀ ʙɪsᴀ ᴘʟᴀʏ ʙᴏᴛ ɪɴɪ ᴋᴀᴋ**",
            reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton("••ꜱɪʟᴀʜᴋᴀɴ ɢᴀʙᴜɴɢ••", url=link)]]
                        ),
            )
        except Exception as e:
            return await message.reply(f"**ERROR :** {e}")

