import sys
from pyrogram import Client
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.errors import RPCError, ChatWriteForbidden, PeerIdInvalid, ChannelPrivate, UserNotParticipant

import config
from ..logging import LOGGER
from YukkiMusic.utils.log_resolver import resolve_log_chat_id


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
        # 1) Resolve ID dari angka/@username/link
        log_value = getattr(config, "LOG_GROUP_ID", None) or getattr(config, "LOG_GROUP", None)
        resolved_log_id = await resolve_log_chat_id(self, log_value)
        config.LOG_GROUP_ID = resolved_log_id  # simpan agar modul lain pakai angka final
        LOGGER(__name__).info(f"[LOG] Resolved LOG_GROUP_ID = {resolved_log_id}")

        # 2) Pastikan bot sudah join & cek izin minimal
        try:
            member = await self.get_chat_member(resolved_log_id, self.id)
        except UserNotParticipant:
            raise RuntimeError("Bot belum menjadi member logger. Tambahkan bot ke grup/channel log.")

        chat = await self.get_chat(resolved_log_id)

        # Channel: wajib Post messages
        if chat.type == ChatType.CHANNEL:
            if member.status != ChatMemberStatus.ADMINISTRATOR:
                raise RuntimeError("Di channel, bot harus Admin dan diizinkan Post messages.")
            priv = getattr(member, "privileges", None)
            if not (priv and getattr(priv, "can_post_messages", False)):
                raise RuntimeError("Izin 'Post messages' untuk bot di channel belum diaktifkan.")

        # Supergroup: tidak wajib admin untuk sekadar kirim (tapi banyak setup butuh admin)
        # Kalau kamu memang ingin wajib admin di grup, uncomment blok di bawah:
        # if chat.type == ChatType.SUPERGROUP and member.status not in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
        #     raise RuntimeError("Di grup log, bot sebaiknya Admin agar semua fitur log berjalan.")

        # 3) Tes kirim pesan supaya ketahuan kalau masih terblok
        await self.send_message(resolved_log_id, "✅ Bot online (log OK).")

    async def start(self):
        await super().start()

        me = await self.get_me()
        self.username = me.username
        self.id = me.id
        self.name = f"{me.first_name} {me.last_name or ''}".strip()
        self.mention = me.mention

        try:
            await self._ensure_log_group_access()
        except ChatWriteForbidden as e:
            LOGGER(__name__).error(f"[LOG] CHAT_WRITE_FORBIDDEN: {e}")
            sys.exit(1)
        except PeerIdInvalid as e:
            LOGGER(__name__).error(f"[LOG] PEER_ID_INVALID (ID/username salah): {e}")
            sys.exit(1)
        except ChannelPrivate as e:
            LOGGER(__name__).error(f"[LOG] CHANNEL_PRIVATE (channel privat & bot belum admin/member): {e}")
            sys.exit(1)
        except RPCError as e:
            LOGGER(__name__).error(f"[LOG] RPCError: {type(e).__name__}: {e}")
            sys.exit(1)
        except Exception as e:
            LOGGER(__name__).error(f"[LOG] Error: {type(e).__name__}: {e}")
            sys.exit(1)

        # (opsional) set perintah
        if config.SET_CMDS:
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
                    BotCommand("playmode","Aʟʟᴏᴡs ʏᴏᴜ ᴛᴏ ᴄʜᴀɴɢᴇ ᴛʜᴇ ᴅᴇғᴀᴜʟᴛ ᴘʟᴀʏᴍᴏᴅᴇ ғᴏʀ ʏᴏᴜʀ ᴄʜᴀᴛ"),
                    BotCommand("settings","Oᴘᴇɴ ᴛʜᴇ sᴇᴛᴛɪɴɢs ᴏғ ᴛʜᴇ ᴍᴜsɪᴄ ʙᴏᴛ ғᴏʀ ʏᴏᴜʀ ᴄʜᴀᴛ."),
                ])
            except Exception as e:
                LOGGER(__name__).warning(f"[SET_CMDS] Gagal set bot commands: {e}")

        # Validasi admin (opsional & fleksibel)
        try:
            a = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
            if a.status not in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER) and a.chat.type == ChatType.CHANNEL:
                LOGGER(__name__).error("Di channel log, bot harus admin.")
                sys.exit(1)
        except Exception as e:
            LOGGER(__name__).warning(f"[LOG] Cek admin melewati karena: {e}")

        LOGGER(__name__).info(f"MusicBot Started as {self.name}")