from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from config import *
from plugins.db import db
from pyrogram.errors import RPCError

async def get_fsub(bot, message):
    user_id = message.from_user.id
    not_joined = []

    for channel_id in AUTH_CHANNELS:
        try:
            member = await bot.get_chat_member(channel_id, user_id)

            if member.status in ["left", "kicked", "restricted"]:
                not_joined.append(channel_id)
        
        except RPCError:
            not_joined.append(channel_id)

    if not not_joined:
        return True

    buttons = []
    for channel_id in not_joined:
        try:
            chat = await bot.get_chat(channel_id)
            channel_link = chat.invite_link
            
            if not channel_link:
                raise ValueError("No invite link available")

        except Exception:
            channel_link = "https://telegram.me/storm_techh"

        buttons.append([InlineKeyboardButton(f"🔔 Join {chat.title}", url=channel_link)])

    await message.reply(
        f"🔮 ʜᴇʟʟᴏ {message.from_user.mention()}, Welcome!\n\n"
        "📢 ᴛʜɪs ɪs sᴛᴏʀᴍ sᴛʀɪɴɢ ɢᴇɴᴇʀᴛᴏʀ ✨\n\n"
        "ғᴏʀ ᴋᴇᴇᴘ ᴜsɪɴɢ ᴀʟʟ ᴛʜᴇ ᴀᴍᴀᴢɪɴɢ ғᴇᴀᴛᴜʀᴇs ɪ ᴏғғᴇʀ, Pʟᴇᴀsᴇ ᴊᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟs. "
        "ᴛʜɪs ʀᴇᴍᴀɪɴ  keep you informed and ensures top-notch service just for you! 😊\n\n"
        "🚀 Join now and dive into a world of knowledge and creativity!",
        reply_markup=InlineKeyboardMarkup(buttons),
    )
    return False

@Client.on_message(filters.private & filters.incoming & filters.command("start"))
async def start(bot: Client, msg: Message):
    if not await db.is_user_exist(msg.from_user.id):
        await db.add_user(msg.from_user.id, msg.from_user.first_name)
        await bot.send_message(
            chat_id=LOG_CHANNEL, 
            text=f"**#NewUser\n\n👤 {msg.from_user.mention}**\n\nID - `{msg.from_user.id}`"
        )
    if not await get_fsub(bot, msg):
        return

    await bot.send_message(
        chat_id=msg.chat.id,
        text=f"""{msg.from_user.mention},\n\nɪ ᴄᴀɴ ɢᴇɴᴇʀᴀᴛᴇ ᴘʏʀᴏɢʀᴀᴍ ᴀɴᴅ ᴛᴇʟᴇᴛʜᴏɴ ꜱᴛʀɪɴɢ ꜱᴇꜱꜱɪᴏɴ\n\nᴜꜱᴇ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴛᴏ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴛʀɪɴɢ sᴇssɪᴏɴ\n\n<blockquote><b>ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ : <a href='https://telegram.me/ll_KEX_ll'>ᴋᴇxx</a></b></blockquote>""",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text="ɢᴇɴᴇʀᴀᴛᴇ sᴛʀɪɴɢ sᴇssɪᴏɴ", callback_data="generate")]
        ])
    )
