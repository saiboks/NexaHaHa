import asyncio, os, time, aiohttp
from asyncio import sleep
from AnonXMusic import app
from pyrogram import filters, Client, enums
from pyrogram.enums import ParseMode
from pyrogram.types import *
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent
from typing import Union, Optional



INFO_TEXT = """
<u><b>ᴜsᴇʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b></u>
<b>● ᴜsᴇʀ ɪᴅ ➠</b> <code>{}</code>
<b>● ᴜsᴇʀɴᴀᴍᴇ ➠</b> <code>@{}</code>
<b>● ᴍᴇɴᴛɪᴏɴ ➠</b> {}
<b>● ᴜsᴇʀ sᴛᴀᴛᴜs ➠</b> {}
<b>● ᴜsᴇʀ ᴅᴄ ɪᴅ ➠</b> {}
"""

# --------------------------------------------------------------------------------- #

async def userstatus(user_id):
   try:
      user = await app.get_users(user_id)
      x = user.status
      if x == enums.UserStatus.RECENTLY:
         return "recently."
      elif x == enums.UserStatus.LAST_WEEK:
          return "last week."
      elif x == enums.UserStatus.LONG_AGO:
          return "seen long ago."
      elif x == enums.UserStatus.OFFLINE:
          return "User is offline."
      elif x == enums.UserStatus.ONLINE:
         return "User is online."
   except:
        return "**✦ sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ !**"

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(["info", "information", "userinfo"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]))
async def userinfo(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not message.reply_to_message and len(message.command) == 2:
        try:
            user_id = message.text.split(None, 1)[1]
            user_info = await app.get_chat(user_id)
            user = await app.get_users(user_id)
            status = await userstatus(user.id)
            id = user_info.id
            dc_id = user.dc_id
            name = user_info.first_name
            username = user_info.username
            mention = user.mention
            bio = user_info.bio
            await app.send_message(chat_id, text=INFO_TEXT.format(
                id, username, mention, status, dc_id), reply_to_message_id=message.id)
        except Exception as e:
            await message.reply_text(str(e))        

    elif not message.reply_to_message:
        try:
            user_info = await app.get_chat(user_id)
            user = await app.get_users(user_id)
            status = await userstatus(user.id)
            id = user_info.id
            dc_id = user.dc_id
            name = user_info.first_name
            username = user_info.username
            mention = user.mention
            bio = user_info.bio
            await app.send_message(chat_id, text=INFO_TEXT.format(
                id, username, mention, status, dc_id), reply_to_message_id=message.id)
        except Exception as e:
            await message.reply_text(str(e))


    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        try:
            user_info = await app.get_chat(user_id)
            user = await app.get_users(user_id)
            status = await userstatus(user.id)
            id = user_info.id
            dc_id = user.dc_id
            name = user_info.first_name
            username = user_info.username
            mention = user.mention
            bio = user_info.bio
            await app.send_message(chat_id, text=INFO_TEXT.format(
                id, username, mention, status, dc_id), reply_to_message_id=message.id)
        except Exception as e:
            await message.reply_text(str(e))