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
        admin_bots = []
        non_admin_bots = []
        
        # Iterate through the bots in the chat
        async for bot in app.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.BOTS):
            if bot.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                admin_bots.append(bot.user)
            else:
                non_admin_bots.append(bot.user)
        
        # Constructing the message
        text3 = f"<b>⬤ ʙᴏᴛ ʟɪsᴛ ➠</b> {message.chat.title}\n\n"

        # Admin bots section
        if admin_bots:
            text3 += "<b>⬤ 🤖 ᴀᴅᴍɪɴ ʙᴏᴛs</b>\n"
            for bot in admin_bots[:-1]:
                text3 += f"<b>├</b> @{bot.username}\n"
            text3 += f"<b>└</b> @{admin_bots[-1].username}\n\n"
        else:
            text3 += "<b>⬤ 🤖 ᴀᴅᴍɪɴ ʙᴏᴛs ➠ ɴᴏɴᴇ</b>\n\n"

        # Non-admin bots section
        if non_admin_bots:
            text3 += "<b>⬤ 🤖 ɴᴏɴ-ᴀᴅᴍɪɴ ʙᴏᴛs</b>\n"
            for bot in non_admin_bots[:-1]:
                text3 += f"<b>├</b> @{bot.username}\n"
            text3 += f"<b>└</b> @{non_admin_bots[-1].username}\n\n"
        else:
            text3 += "<b>⬤ 🤖 ɴᴏɴ-ᴀᴅᴍɪɴ ʙᴏᴛs ➠ ɴᴏɴᴇ</b>\n\n"

        # Total bot count
        total_bots = len(admin_bots) + len(non_admin_bots)
        text3 += f"<b>⬤ ᴛᴏᴛᴀʟ ɴᴜᴍʙᴇʀ ᴏғ ʙᴏᴛs ➠</b> {total_bots}"

        await app.send_message(message.chat.id, text3)

    except FloodWait as e:
        await asyncio.sleep(e.value)