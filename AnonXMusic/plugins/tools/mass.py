import asyncio
from time import time
import os
import sys
from pyrogram import Client, enums
from pyrogram import filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import ChatPermissions, ChatPrivileges, Message
from AnonXMusic import app
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.errors import MessageDeleteForbidden, RPCError
from config import OWNER_ID 

# Muteall
@app.on_message(filters.command("muteall", prefixes=[".", "!", "/"]) & filters.group)
async def mute_all(client, message):
    del_u = 0
    admin = await is_administrator(message.from_user.id, message, client)
    owner = await is_owner(message.from_user.id, message, client)

    if not admin or owner:
        return await message.edit("Sorry, you are not allowed to use this command!")  # Edit original message

    response_message = await message.edit("Muting all members...")

    async for user in client.get_chat_members(message.chat.id):
        if user.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.RESTRICTED] and not await is_administrator(user.user.id, message, client) and not await is_owner(user.user.id, message, client):
            try:
                await client.restrict_chat_member(
                    message.chat.id,
                    user.user.id,
                    permissions=ChatPermissions()  # No permissions, hence muted
                )
                del_u += 1
            except ChatAdminRequired:
                return await response_message.edit("Do not have permission to mute in this group.")  # Edit original message
            except Exception as e:
                print(f"Error muting user {user.user.id}: {e}")

    final_count = len([user async for user in client.get_chat_members(message.chat.id)])
    del_status = f"Muted {del_u} members" if del_u > 0 else "No members to mute."
    await response_message.edit(del_status)
    await asyncio.sleep(5)  # Change to 5 seconds
    await response_message.delete()


# Unmuteall
@app.on_message(filters.command("unmuteall", prefixes=[".", "!", "/"]) & filters.group)
async def unmute_all(client, message):
    del_u = 0
    admin = await is_administrator(message.from_user.id, message, client)
    owner = await is_owner(message.from_user.id, message, client)

    if not admin or owner:
        return await message.edit("Sorry, you are not allowed to use this command!")  # Edit original message

    response_message = await message.edit("Unmuting all members...")
    initial_count = len([user async for user in client.get_chat_members(message.chat.id)])

    async for user in client.get_chat_members(message.chat.id):
        try:
            member = await client.get_chat_member(message.chat.id, user.user.id)
            if member.status == ChatMemberStatus.RESTRICTED:
                if not await is_administrator(user.user.id, message, client) and not await is_owner(user.user.id, message, client):
                    try:
                        await client.restrict_chat_member(
                            message.chat.id,
                            user.user.id,
                            permissions=ChatPermissions(
                                can_send_messages=True,
                                can_send_media_messages=True,
                                can_send_other_messages=True,
                                can_send_polls=True,
                                can_add_web_page_previews=True,
                            ),
                        )
                        del_u += 1
                    except ChatAdminRequired:
                        return await response_message.edit("Do not have permission to unmute in this group.")  # Edit original message
                    except Exception as e:
                        print(f"Error unmuting user {user.user.id}: {e}")
                    await asyncio.sleep(1)
        except Exception as e:
            print(f"Error retrieving user {user.user.id}: {e}")

    final_count = len([user async for user in client.get_chat_members(message.chat.id)])
    del_status = f"Unmuted {del_u} members" if del_u > 0 else "No members to unmute."
    await response_message.edit(del_status)
    await asyncio.sleep(5)  # Change to 5 seconds
    await response_message.delete()