import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram import enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait
from AnonXMusic import app


@app.on_message(filters.command("bots"))
async def bots(client, message):  
  try:    
    botList = []
    async for bot in app.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.BOTS):
      botList.append(bot.user)
    lenBotList = len(botList) 
    text3  = f"<b>⬤ ʙᴏᴛ ʟɪsᴛ ➠</b> {message.chat.title}\n\n<b>⬤ 🤖 ʙᴏᴛs</b>\n"
    while len(botList) > 1:
      bot = botList.pop(0)
      text3 += f"<b>├</b> @{bot.username}\n"    
    else:    
      bot = botList.pop(0)
      text3 += f"<b>└</b> @{bot.username}\n\n"
      text3 += f"<b>⬤ ᴛᴏᴛᴀʟ ɴᴜᴍʙᴇʀ ᴏғ ʙᴏᴛs ➠</b> {lenBotList}"  
      await app.send_message(message.chat.id, text3)
  except FloodWait as e:
    await asyncio.sleep(e.value)