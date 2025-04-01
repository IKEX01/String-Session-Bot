from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from config import *
from plugins.db import db
from pyrogram.errors import RPCError

async def get_fsub(bot: Client, message: Message):
    user_id = message.from_user.id
    not_joined = []

    for channel_id in AUTH_CHANNELS:
        try:
            member = await bot.get_chat_member(channel_id, user_id)
            if member.status in ["left", "kicked", "restricted"]:
                not_joined.append(channel_id)
        except RPCError:
            not_joined.append(channel_id)
        except Exception as e:
            print(f"ᴇʀʀᴏʀ ғᴇᴛᴄʜɪɴɢ ᴍᴇᴍʙᴇʀ sᴛᴀᴛᴜs ғᴏʀ {channel_id}: {e}")
            not_joined.append(channel_id)

    if not not_joined:
        return True

    buttons = []
    for channel_id in not_joined:
        try:
            chat = await bot.get_chat(channel_id)
            channel_link = chat.invite_link or (f"https://telegram.me/{chat.username}" if chat.username else None)

            if channel_link:
                buttons.append([InlineKeyboardButton(f"🔔 ᴊᴏɪɴ {chat.title}", url=channel_link)])
            else:
                raise ValueError("ɴᴏ ᴠᴀʟɪᴅ ɪɴᴠɪᴛᴇ ʟɪɴᴋ ᴏʀ ɪᴛ ɪs ᴄʜᴀɴɢᴇᴅ ʙʏ ʙᴏᴛ ᴏᴡɴᴇʀ.")

        except Exception as e:
            print(f"Error fetching chat details for {channel_id}: {e}")
            buttons.append([InlineKeyboardButton("🔔 ᴊᴏɪɴ ɪɢɴɪᴛᴇ ᴛᴇᴄʜ", url="https://telegram.me/igniteUnity")])

    await message.reply(
        text=(
            f"🔮 ʜᴇʟʟᴏ {message.from_user.mention()}, ᴡᴇʟᴄᴏᴍᴇ!\n\n"
            "📢 ᴛʜɪs ɪs Sᴛᴏʀᴍ Sᴛʀɪɴɢ Gᴇɴᴇʀᴀᴛᴏʀ ✨\n\n"
            "ғᴏʀ ᴋᴇᴇᴘ ᴜsɪɴɢ ᴀʟʟ ᴛʜᴇ ᴀᴍᴀᴢɪɴɢ ғᴇᴀᴛᴜʀᴇs ɪ ᴏғғᴇʀ, ᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟs.\n"
            "ᴛᴏ ʀᴇᴍᴀɪɴ ʏᴏᴜ ɪɴғᴏʀᴍᴇᴅ ᴀɴᴅ ᴇɴsᴜʀᴇs ᴀᴄᴛ ᴏғ ᴀssɪsᴛᴀɴᴄᴇ ᴊᴜsᴛ ғᴏʀ ʏᴏᴜ! 😊\n\n"
            "🚀 ᴊᴏɪɴ ɴᴏᴡ ᴀɴᴅ ғʟʏ ɪɴᴛᴏ ᴀ ᴡᴏʀʟᴅ ᴏғ ᴠᴇʀsɪʟɪᴛʏ ᴀɴᴅ ɪᴍᴀɢɪɴᴀᴛɪᴏɴ!"
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
    )
    return False

@Client.on_message(filters.private & filters.incoming & filters.command("start"))
async def start(bot: Client, msg: Message):
    if not await db.is_user_exist(msg.from_user.id):
        await db.add_user(msg.from_user.id, msg.from_user.first_name)
        await bot.send_message(
            chat_id=LOG_CHANNEL, 
            text=f"**#ɴᴇᴡᴜsᴇʀ\n\n👤 {msg.from_user.mention}**\n\nɪᴅ - `{msg.from_user.id}`"
        )
    
    if not await get_fsub(bot, msg):
        return

    await bot.send_message(
        chat_id=msg.chat.id,
        text=(
            f"{msg.from_user.mention},\n\n"
            "ɪ ᴄᴀɴ ɢᴇɴᴇʀᴀᴛᴇ ᴘʏʀᴏɢʀᴀᴍ ᴀɴᴅ ᴛᴇʟᴇᴛʜᴏɴ ꜱᴛʀɪɴɢ ꜱᴇꜱꜱɪᴏɴ\n\n"
            "ᴜꜱᴇ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴛᴏ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴛʀɪɴɢ sᴇssɪᴏɴ\n\n"
            "<blockquote><b>ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ : <a href='https://telegram.me/ll_KEX_ll'>ᴋᴇxx</a></b></blockquote>"
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text="ɢᴇɴᴇʀᴀᴛᴇ sᴛʀɪɴɢ sᴇssɪᴏɴ", callback_data="ɢᴇɴᴇʀᴀᴛᴇ")]
        ])
    )
