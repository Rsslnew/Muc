import os
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegraph import upload_file
from YukkiMusic import app


@app.on_message(filters.command(["tgm", "tgt", "telegraph", "tl"]))
async def get_link_group(client, message):
    if not message.reply_to_message:
        return await message.reply_text(
            "ʀᴇᴘʟʏ ɢᴀᴍʙᴀʀ ᴍᴜ ᴜɴᴛᴜᴋ ᴅɪᴊᴀᴅɪᴋᴀɴ ʟɪɴᴋ ᴛɢ"
        )
    try:
        text = await message.reply("ᴘʀᴏᴄᴇssɪɴɢ...")

        async def progress(current, total):
            await text.edit_text(f"📥 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ... {current * 100 / total:.1f}%")

        try:
            location = f"cache"
            local_path = await message.reply_to_message.download(
                location, progress=progress
            )
            await text.edit_text("📤 ᴜᴘʟᴏᴀᴅɪɴɢ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴘʜ...")
            upload_path = upload_file(local_path)
            await text.edit_text(
                f"🌐 | [ᴛᴇʟᴇɢʀᴀᴘʜ ʟɪɴᴋ](https://telegra.ph{upload_path[0]})",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "ᴛᴇʟᴇɢʀᴀᴘʜ ʟɪɴᴋ",
                                url=f"https://telegra.ph{upload_path[0]}",
                            )
                        ]
                    ]
                ),
            )
            os.remove(local_path)
        except Exception as e:
            await text.edit_text(f"❌ |ғɪʟᴇ ᴜᴘʟᴏᴀᴅ ғᴀɪʟᴇᴅ \n\n<i>ʀᴇᴀsᴏɴ: {e}</i>")
            os.remove(local_path)
            return
    except Exception:
        pass