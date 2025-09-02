# YukkiMusic/core/bot.py
import sys
from pyrogram import Client
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.types import BotCommand
from pyrogram.errors import (
    ChatWriteForbidden,
    PeerIdInvalid,
    ChannelPrivate,
    UserNotParticipant,
    RPCError,
)

import config
from ..logging import LOGGER
from YukkiMusic.utils.log_resolver import resolve_log_chat_id


def as_bool(v):
    if isinstance(v, bool):
        return v
    if v is None:
        return False
    return str(v).strip().lower() in {"1", "true", "yes", "y", "on"}


class YukkiBot(Client):
    def __init__(self):
        LOGGER(__name__).info("Starting Bot")
        super().__init__(
            "YukkiMusicBot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            workdir="datafiles",
            max_concurrent_transmissions=7,
        )

    async def _ensure_log_group_access(self):
        # 1) Resolve LOG_GROUP_ID: angka / string / @username / t.me/...
        log_value = getattr(config, "LOG_GROUP_ID", None) or getattr(config, "LOG_GROUP", None)
        resolved_log_id = await resolve_log_chat_id(self, log_value)
        config.LOG_GROUP_ID = resolved_log_id  # simpan untuk modul lain

        # 2) Kirim pesan start ke logger (sekalian ngetes izin kirim)
        me = await self.get_me()
        start_text = (
            f"<u><b>{me.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b></u>\n\n"
            f"ɪᴅ : <code>{me.id}</code>\n"
            f"ɴᴀᴍᴇ : {me.first_name} {(me.last_name or '')}\n"
            f"ᴜsᴇʀɴᴀᴍᴇ : @{me.username}"
        )
        await self.send_message(resolved_log_id, start_text)

        # 3) Cek membership & izin seperlunya
        try:
            member = await self.get_chat_member(resolved_log_id, me.id)
        except UserNotParticipant:
            raise RuntimeError("Bot belum menjadi member logger. Tambahkan bot ke grup/channel log.")

        chat = await self.get_chat(resolved_log_id)
        if chat.type == ChatType.CHANNEL:
            # Channel: wajib admin + Post messages
            if member.status != ChatMemberStatus.ADMINISTRATOR:
                raise RuntimeError("Di channel, bot harus Admin dengan izin 'Post messages'.")
            priv = getattr(member, "privileges", None)
            if not (priv and getattr(priv, "can_post_messages", False)):
                raise RuntimeError("Izin 'Post messages' untuk bot di channel belum diaktifkan.")

    async def start(self):
        await super().start()

        me = await self.get_me()
        self.username = me.username
        self.id = me.id
        self.name = f"{me.first_name} {(me.last_name or '')}".strip()
        self.mention = me.mention

        # Pastikan akses logger jelas error-nya (tidak ditelan)
        try:
            await self._ensure_log_group_access()
        except ChatWriteForbidden as e:
            LOGGER(__name__).error(f"[LOG] CHAT_WRITE_FORBIDDEN: {e}")
            sys.exit(1)
        except PeerIdInvalid as e:
            LOGGER(__name__).error(f"[LOG] PEER_ID_INVALID (ID/username salah): {e}")
            sys.exit(1)
        except ChannelPrivate as e:
            LOGGER(__name__).error(f"[LOG] CHANNEL_PRIVATE (channel privat & bot bukan admin/member): {e}")
            sys.exit(1)
        except RPCError as e:
            LOGGER(__name__).error(f"[LOG] RPCError {type(e).__name__}: {e}")
            sys.exit(1)
        except Exception as e:
            LOGGER(__name__).error(f"[LOG] Error: {type(e).__name__}: {e}")
            sys.exit(1)

        # (opsional) set perintah
        if as_bool(getattr(config, "SET_CMDS", False)):
            try:
                await self.set_bot_commands([
                    BotCommand("start", "start the bot"),
                    BotCommand("ping", "ᴄʜᴇᴄᴋ ʙᴏᴛ ɪs ᴀʟɪᴠᴇ ᴏʀ ᴅᴇᴀᴅ"),
                    BotCommand("play", "sᴛᴀʀᴛ ᴘʟᴀʏɪɴɢ ʀᴇǫᴜᴇᴛᴇᴅ sᴏɴɢ"),
                    BotCommand("skip", "ᴍᴏᴠᴇ ᴛᴏ ɴᴇxᴛ ᴛʀᴀᴄᴋ ɪɴ ǫᴜᴇᴜᴇ"),
                    BotCommand("pause", "ᴘʟᴀᴜsᴇ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴘʟᴀʏɪɴɢ sᴏɴɢ"),
                    BotCommand("resume", "ʀᴇsᴜᴍᴇ ᴛʜᴇ ᴘᴀᴜsᴇᴅ sᴏɴɢ"),
                    BotCommand("end", "ᴄʟᴇᴀʀ ᴛʜᴇ ǫᴜᴇᴜᴇ ᴀᴍᴅ ʟᴇᴀᴠᴇ ᴠᴏɪᴄᴇᴄʜᴀᴛ"),
                    BotCommand("shuffle", "Rᴀɴᴅᴏᴍʟʏ sʜᴜғғʟᴇs ᴛʜᴇ ǫᴜᴇᴜᴇᴅ ᴘʟᴀʏʟɪsᴛ."),
                    BotCommand("playmode", "Aʟʟᴏᴡs ʏᴏᴜ ᴛᴏ ᴄʜᴀɴɢᴇ ᴛʜᴇ ᴅᴇғᴀᴜʟᴛ ᴘʟᴀʏᴍᴏᴅᴇ ғᴏʀ ʏᴏᴜʀ ᴄʜᴀᴛ"),
                    BotCommand("settings", "Oᴘᴇɴ ᴛʜᴇ sᴇᴛᴛɪɴɢs ᴏғ ᴛʜᴇ ᴍᴜsɪᴄ ʙᴏᴛ ғᴏʀ ʏᴏᴜʀ ᴄʜᴀᴛ."),
                ])
            except Exception as e:
                LOGGER(__name__).warning(f"[SET_CMDS] Gagal set bot commands: {e}")

        LOGGER(__name__).info(f"MusicBot Started as {self.name}")