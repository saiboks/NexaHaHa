from pyrogram import filters, Client
from pyrogram.types import ChatPrivileges, ChatPermissions, Message
from pyrogram.types import *
from pyrogram.enums import ChatMembersFilter, ChatType
from datetime import datetime, timedelta, timezone
import asyncio
import logging

# Check if user has admin rights
async def is_administrator(user_id: int, message,client):
    admin = False
    administrators = []
    async for m in app.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
        administrators.append(m)
    for user in administrators:
        if user.user.id == user_id:
            admin = True
            break
    return admin
async def is_admin(user_id: int, message):

    administrators = []
    async for m in app.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
        administrators.append(m)
    if user_id in administrators:
        return True     
    else:
        return False


@Client.on_message(filters.command(["promote", "fullpromote"], ".") & ~filters.private & filters.me)
async def promoteFunc(client, message):
    try:
        if message.reply_to_message:
            user = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            user = message.text.split(None, 1)[1]
        else:
            await message.edit_text("Invalid command usage.")
            await asyncio.sleep(5)
            await message.delete()
            return

        umention = (await client.get_users(user)).mention
    except Exception:
        await message.edit_text("Invalid ID or user not found.")
        await asyncio.sleep(5)
        await message.delete()
        return

    if not user:
        await message.edit_text("User not found.")
        await asyncio.sleep(5)
        await message.delete()
        return

    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if user == client.me.id:
        await message.edit_text("You cannot promote yourself.")
        await asyncio.sleep(5)
        await message.delete()
        return

    if not bot or not bot.can_promote_members:
        await message.edit_text("I don't have the permission to promote members.")
        await asyncio.sleep(5)
        await message.delete()
        return

    try:
        if message.command[0] == "fullpromote":
            await message.chat.promote_member(
                user_id=user,
                privileges=ChatPrivileges(
                    can_change_info=bot.can_change_info,
                    can_invite_users=bot.can_invite_users,
                    can_delete_messages=bot.can_delete_messages,
                    can_restrict_members=bot.can_restrict_members,
                    can_pin_messages=bot.can_pin_messages,
                    can_promote_members=bot.can_promote_members,
                    can_manage_chat=bot.can_manage_chat,
                    can_manage_video_chats=bot.can_manage_video_chats,
                ),
            )
            final_msg = await message.edit_text("User has been fully promoted.")
        else:
            await message.chat.promote_member(
                user_id=user,
                privileges=ChatPrivileges(
                    can_change_info=False,
                    can_invite_users=bot.can_invite_users,
                    can_delete_messages=bot.can_delete_messages,
                    can_restrict_members=False,
                    can_pin_messages=bot.can_pin_messages,
                    can_promote_members=False,
                    can_manage_chat=bot.can_manage_chat,
                    can_manage_video_chats=bot.can_manage_video_chats,
                ),
            )
            final_msg = await message.edit_text("User has been promoted.")
    except Exception as err:
        await message.edit_text(f"An error occurred: {err}")
        await asyncio.sleep(5)
        await message.delete()
    else:
        await asyncio.sleep(5)
        await final_msg.delete()


@Client.on_message(filters.command(["demote"], ".") & ~filters.private & filters.me)
async def demoteFunc(client, message):
    try:
        if message.reply_to_message:
            user = message.reply_to_message.from_user.id
        elif not message.reply_to_message and len(message.command) != 1:
            user = message.text.split(None, 1)[1]

        umention = (await client.get_users(user)).mention
    except:
        error_msg = await message.edit("Invalid ID")
        await asyncio.sleep(5)
        return await error_msg.delete()

    try:
        await message.chat.promote_member(user_id=user,
            privileges=ChatPrivileges(
                can_change_info=False,
                can_invite_users=False,
                can_delete_messages=False,

                can_restrict_members=False,
                can_pin_messages=False,
                can_promote_members=False,
                can_manage_chat=False,
                can_manage_video_chats=False,
            ))
        success_msg = await message.edit("Successfully Demoted")
        await asyncio.sleep(5)
        await success_msg.delete()
    except Exception as err:
        error_msg = await message.edit(f"Error: {err}")
        await asyncio.sleep(5)
        await error_msg.delete()