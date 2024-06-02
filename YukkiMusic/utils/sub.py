from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from YukkiMusic import app
from config import JOIN_HELA


async def subcribe(client, message):
    if not JOIN_HELA:
        return

    try:
        await app.get_chat_member(config.JOIN_HELA, message.from_user.id)
    except UserNotParticipant:
        try:
            link = f"t.me/{config.JOIN_DULU}"
            await message.reply(
                f"**ʜᴀʟʟᴏ ᴋᴀᴋ😊 {message.from_user.mention} ᴀɢᴀʀ ʙɪsᴀ ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ ʙᴏᴛ ᴀɴᴅᴀ ʜᴀʀᴜs ᴍᴀsᴜᴋ ᴋᴇ ɢʀᴏᴜᴘ ᴛᴇʀʟᴇʙɪʜ ᴅᴀʜᴜʟᴜ!. sɪʟᴀʜᴋᴀɴ ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ ᴅɪ ʙᴀᴡᴀʜ ᴜɴᴛᴜᴋ ᴊᴏɪɴ ᴋᴇ ɢʀᴏᴜᴘ, sᴇᴛᴇʟᴀʜ ɪᴛᴜ sɪʟᴀʜᴋᴀɴ ᴘʟᴀʏ ᴍᴜsɪᴋ/ᴠɪᴅᴇᴏ ᴋᴀᴍᴜ**",
            reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton("••ꜱɪʟᴀʜᴋᴀɴ ᴊᴏɪɴ••", url=link)]]
                        ),
            )
        except Exception as e:
            return await message.reply(f"**ERROR :** {e}")

