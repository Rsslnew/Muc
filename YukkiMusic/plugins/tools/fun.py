import requests
from pyrogram import filters
from pyrogram.types import Message

from YukkiMusic import app


@app.on_message(
    filters.command(
        [
            "dice",
            "ludo",
            "dart",
            "basket",
            "basketball",
            "football",
            "slot",
            "bowling",
            "jackpot",
            "afk",
            "cp",
        ]
    )
)
async def dice(c, m: Message):
    command = m.text.split()[0]
    if command == "/dice" or command == "/ludo":

        value = await c.send_dice(m.chat.id, reply_to_message_id=m.id)
        await value.reply_text("ʏᴏᴜʀ sᴄᴏʀᴇ ɪs {0}".format(value.dice.value))

    elif command == "/dart":

        value = await c.send_dice(m.chat.id, emoji="🎯", reply_to_message_id=m.id)
        await value.reply_text("ʏᴏᴜʀ sᴄᴏʀᴇ ɪs {0}".format(value.dice.value))

    elif command == "/basket" or command == "/basketball":
        basket = await c.send_dice(m.chat.id, emoji="🏀", reply_to_message_id=m.id)
        await basket.reply_text("ʏᴏᴜʀ sᴄᴏʀᴇ ɪs {0}".format(basket.dice.value))

    elif command == "/football":
        value = await c.send_dice(m.chat.id, emoji="⚽", reply_to_message_id=m.id)
        await value.reply_text("ʏᴏᴜʀ sᴄᴏʀᴇ ɪs {0}".format(value.dice.value))

    elif command == "/slot" or command == "/jackpot":
        value = await c.send_dice(m.chat.id, emoji="🎰", reply_to_message_id=m.id)
        await value.reply_text("ʏᴏᴜʀ sᴄᴏʀᴇ ɪs {0}".format(value.dice.value))
    elif command == "/bowling":
        value = await c.send_dice(m.chat.id, emoji="🎳", reply_to_message_id=m.id)
        await value.reply_text("ʏᴏᴜʀ sᴄᴏʀᴇ ɪs {0}".format(value.dice.value))


bored_api_url = "https://apis.scrimba.com/bored/api/activity"


@app.on_message(filters.command("bored", prefixes="/"))
async def bored_command(client, message):
    response = requests.get(bored_api_url)
    if response.status_code == 200:
        data = response.json()
        activity = data.get("activity")
        if activity:
            await message.reply(f"𝗙𝗲𝗲𝗹𝗶𝗻𝗴 𝗯𝗼𝗿𝗲𝗱? 𝗛𝗼𝘄 𝗮𝗯𝗼𝘂𝘁:\n\n {activity}")
        else:
            await message.reply("Nᴏ ᴀᴄᴛɪᴠɪᴛʏ ғᴏᴜɴᴅ.")
    else:
        await message.reply("Fᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ ᴀᴄᴛɪᴠɪᴛʏ.")


__MODULE__ = "ᴇxᴛʀᴀ"
__HELP__ = """
/bored - ɢᴇᴛᴛɪɴɢ ʙᴏʀᴇ ᴛʀʏ ᴛʜɪs ᴄᴏᴍᴍᴀᴍᴅ
/dice - sᴇɴᴅ ᴛʜᴇ 🎲 ᴀɴᴅ ɢᴇᴛ ʏᴏᴜʀ sᴄᴏʀᴇ
/dart - sᴇɴᴅ ᴛʜᴇ 🎯 ᴀɴᴅ ɢᴇᴛ ʏᴏᴜʀ sᴄᴏʀᴇ
/basketball - sᴇɴᴅ ᴛʜᴇ 🏀 ᴀɴᴅ ɢᴇᴛ ʏᴏᴜʀ sᴄᴏʀᴇ
/football - sᴇɴᴅ ᴛʜᴇ ⚽ ᴀɴᴅ ɢᴇᴛ ʏᴏᴜʀ sᴄᴏʀᴇ
/jackpot - sᴇɴᴅ ᴛʜᴇ 🎰 ᴀɴᴅ ɢᴇᴛ ʏᴏᴜʀ sᴄᴏʀᴇ
/bowling - sᴇɴᴅ ᴛʜᴇ  🎳 ᴀɴᴅ ɢᴇᴛ ʏᴏᴜʀ sᴄᴏʀᴇ
/afk - ʀᴇᴘʟʏ ᴘʜᴏᴛᴏ ᴅʟʟ ᴜɴᴛᴜᴋ ᴀғᴋ
/cp - ᴍᴇʟɪʜᴀᴛ ᴘᴀsᴀɴɢᴀɴ ʜᴀʀɪ ɪɴɪ
"""
