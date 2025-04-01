from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid
from plugins.db import db
from pyrogram import Client, filters
from config import OWNER_ID
import asyncio
import datetime
import time

async def broadcast_messages(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await broadcast_messages(user_id, message)
    except InputUserDeactivated:
        await db.delete_user(int(user_id))
        return False, "Deleted"
    except UserIsBlocked:
        await db.delete_user(int(user_id))
        return False, "Blocked"
    except PeerIdInvalid:
        await db.delete_user(int(user_id))
        return False, "Error"
    except Exception as e:
        return False, "Error"

@Client.on_message(filters.command("users") & filters.user(OWNER_ID))
async def users(client, message):
    total_users = await db.total_users_count()
    text = f"**ᴛᴏᴛᴀʟ ᴜsᴇʀs: {total_users}**"
    await message.reply_text(
        text=text,
        quote=True,
        disable_web_page_preview=True
    )

@Client.on_message(filters.command("broadcast") & filters.user(OWNER_ID) & filters.reply)
async def broadcast(bot, message):
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    if not b_msg:
        return await message.reply_text("**Reply This Command To Your Broadcast Message**")
    sts = await message.reply_text(
        text='ᴛʀᴀɴsᴍɪᴛᴛᴇᴅ ʏᴏᴜʀ ᴍᴇssᴀɢᴇs...'
    )
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    blocked = 0
    deleted = 0
    failed =0

    success = 0
    async for user in users:
        if 'id' in user:
            pti, sh = await broadcast_messages(int(user['id']), b_msg)
            if pti:
                success += 1
            elif pti == False:
                if sh == "Blocked":
                    blocked += 1
                elif sh == "Deleted":
                    deleted += 1
                elif sh == "Error":
                    failed += 1
            done += 1
            if not done % 20:
                await sts.edit(f"ᴛʀᴀɴsᴍɪssɪᴏɴ ɪs ᴏɴ ʜɪs ᴡᴀʏ :\n\nᴛᴏᴛᴀʟ ᴜsᴇʀs {total_users}\nCᴏᴍᴘʟᴇᴛᴇᴅ: {done} / {total_users}\nSᴜᴄᴄᴇss: {success}\nʙʟᴏᴄᴋᴇᴅ: {blocked}\nᴅᴇʟᴇᴛᴇᴅ: {deleted}")    
        else:
            # Handle the case where 'id' key is missing in the user dictionary
            done += 1
            failed += 1
            if not done % 20:
                await sts.edit(f"ᴛᴇʟᴇᴄᴀsᴛ ɪs ᴏɴ ᴘʀᴏɢʀᴇssɪᴏɴ:\n\nTᴏᴛᴀʟ Usᴇʀs {total_users}\nCᴏᴍᴘʟᴇᴛᴇᴅ: {done} / {total_users}\nSᴜᴄᴄᴇss: {success}\nBʟᴏᴄᴋᴇᴅ: {blocked}\nDᴇʟᴇᴛᴇᴅ: {deleted}")    
    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.edit(f"Tᴇʟᴇᴄᴀsᴛ ᴅᴏɴᴇ:\nCᴏᴍᴘʟᴇᴛᴇᴅ ɪɴ {time_taken} seconds.\n\nTᴏᴛᴀʟ ᴜsᴇʀs {total_users}\nCᴏᴍᴘʟᴇᴛᴇᴅ: {done} / {total_users}\nSᴜᴄᴄᴇss: {success}\nBʟᴏᴄᴋᴇᴅ: {blocked}\nDᴇʟᴇᴛᴇᴅ: {deleted}")
