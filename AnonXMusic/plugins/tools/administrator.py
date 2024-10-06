import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram import enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait
from AnonXMusic import app


@app.on_message(filters.command(["admins","staff"]))
async def admins(client, message):
  try: 
    adminList = []
    ownerList = []
    async for admin in app.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
      if admin.privileges.is_anonymous == False:
        if admin.user.is_bot == True:
          pass
        elif admin.status == ChatMemberStatus.OWNER:
          ownerList.append(admin.user)
        else:  
          adminList.append(admin.user)
      else:
        pass   
    lenAdminList= len(ownerList) + len(adminList)  
    text2 = f"<b>⬤ ɢʀᴏᴜᴘ sᴛᴀғғ ➠</b> {message.chat.title}\n\n"
    try:
      owner = ownerList[0]
      if owner.username == None:
        text2 += f"<b>⬤ ᴏᴡɴᴇʀ</b>\n<b>└</b> {owner.mention}\n\n<b>👮🏻 ᴀᴅᴍɪɴs</b>\n"
      else:
        text2 += f"<b>⬤ ᴏᴡɴᴇʀ</b>\n<b>└</b> @{owner.username}\n\n<b>⬤👮🏻 ᴀᴅᴍɪɴs</b>\n"
    except:
      text2 += f"<b>⬤ ᴏᴡɴᴇʀ</b>\n<b>└</b> <i>Hidden</i>\n\n<b>👮🏻 ᴀᴅᴍɪɴs</b>\n"
    if len(adminList) == 0:
      text2 += "<b>└</b> <i>ᴀᴅᴍɪɴs ᴀʀᴇ ʜɪᴅᴅᴇɴ</i>"  
      await app.send_message(message.chat.id, text2)   
    else:  
      while len(adminList) > 1:
        admin = adminList.pop(0)
        if admin.username == None:
          text2 += f"<b>├</b> {admin.mention}\n"
        else:
          text2 += f"<b>├</b> @{admin.username}\n"    
      else:    
        admin = adminList.pop(0)
        if admin.username == None:
          text2 += f"<b>└</b> {admin.mention}\n\n"
        else:
          text2 += f"<b>└</b> @{admin.username}\n\n"
      text2 += f"<b>⬤ ᴛᴏᴛᴀʟ ɴᴜᴍʙᴇʀ ᴏғ ᴀᴅᴍɪɴs ➠ {lenAdminList}</b>"  
      await app.send_message(message.chat.id, text2)           
  except FloodWait as e:
    await asyncio.sleep(e.value)       
