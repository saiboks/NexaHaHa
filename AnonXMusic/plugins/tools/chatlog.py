import random
from pyrogram import Client
from pyrogram.types import Message
from pyrogram import filters
from pyrogram.types import(InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, InputMediaVideo, Message)
from config import LOGGER_ID as LOG_GROUP_ID
from AnonXMusic import app  

JOIN = [
"https://unitedcamps.in/Images/file_4111.jpg",
"https://unitedcamps.in/Images/file_4110.jpg",
"https://unitedcamps.in/Images/file_4109.jpg",
"https://unitedcamps.in/Images/file_4108.jpg",   

]

LEFT = [
    "https://unitedcamps.in/Images/file_4107.jpg",
    "https://unitedcamps.in/Images/file_4106.jpg",
    "https://unitedcamps.in/Images/file_4105.jpg",
    "https://unitedcamps.in/Images/file_4104.jpg",    
]



@app.on_message(filters.new_chat_members, group=2)
async def join_watcher(_, message):    
    chat = message.chat
    link = await app.export_chat_invite_link(message.chat.id)
    for members in message.new_chat_members:
        if members.id == app.id:
            count = await app.get_chat_members_count(chat.id)

            msg = (
                f"<b>⬤ ʙᴏᴛ ᴀᴅᴅᴇᴅ ɪɴ ᴀ #ɴᴇᴡ_ɢʀᴏᴜᴘ ⬤</b>\n\n"

                f"<b>● ɢʀᴏᴜᴘ ɴᴀᴍᴇ ➠</b> {message.chat.title}\n"
                f"<b>● ɢʀᴏᴜᴘ ɪᴅ ➠</b> {message.chat.id}\n"
                f"<b>● ɢʀᴏᴜᴘ ᴜsᴇʀɴᴀᴍᴇ ➠</b> @{message.chat.username}\n"
                f"<b>● ɢʀᴏᴜᴘ ʟɪɴᴋ ➠</b> {link}\n"
                f"<b>● ɢʀᴏᴜᴘ ᴍᴇᴍʙᴇʀs ➠</b> {count}\n\n"
                f"<b>⬤ ᴀᴅᴅᴇᴅ ʙʏ ➠</b> {message.from_user.mention}"
            )
            await app.send_photo(LOG_GROUP_ID, photo=random.choice(JOIN), caption=msg, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(f"sᴇᴇ ʙᴏᴛ ᴀᴅᴅᴇᴅ ɢʀᴏᴜᴘ", url=f"{link}")]
         ]))



@app.on_message(filters.left_chat_member)
async def on_left_chat_member(_, message: Message):
    if (await app.get_me()).id == message.left_chat_member.id:
        remove_by = message.from_user.mention if message.from_user else "𝐔ɴᴋɴᴏᴡɴ 𝐔sᴇʀ"
        title = message.chat.title
        username = f"@{message.chat.username}" if message.chat.username else "𝐏ʀɪᴠᴀᴛᴇ 𝐂ʜᴀᴛ"
        chat_id = message.chat.id
        left = f"<b>⬤ ʙᴏᴛ #ʟᴇғᴛ_ɢʀᴏᴜᴘ ʙʏ ᴀ ᴄʜᴜᴛɪʏᴀ ⬤</b>\n\n<b>● ɢʀᴏᴜᴘ ɴᴀᴍᴇ ➠</b> {title}\n\n<b>● ɢʀᴏᴜᴘ ɪᴅ ➠</b> {chat_id}\n\n<b>● ʙᴏᴛ ʀᴇᴍᴏᴠᴇᴅ ʙʏ ➠</b> {remove_by}"
        await app.send_photo(LOG_GROUP_ID, photo=random.choice(LEFT), caption=left, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(f"ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ", url=f"https://t.me/{app.username}?startgroup=true")]
         ]))

#welcome