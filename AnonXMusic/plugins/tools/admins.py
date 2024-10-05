from pyrogram import filters, Client
from AnonXMusic import app
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


@app.on_message(filters.command(["promote", "fullpromote"], "."))
async def promoteFunc(client, message):
    try:
        if message.reply_to_message:
            user = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            user = message.text.split(None, 1)[1]
        else:
            await message.reply("Invalid command usage.")
            return

        umention = (await client.get_users(user)).mention
    except Exception:
        await message.reply("Invalid ID or user not found.")
        return

    if not user:
        await message.reply("User not found.")
        return

    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if user == client.me.id:
        await message.reply("You cannot promote yourself.")
        return

    if not bot or not bot.can_promote_members:
        await message.reply("I don't have the permission to promote members.")
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
            await message.reply("User has been fully promoted.")
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
            await message.reply("User has been promoted.")
    except Exception as err:
        await message.reply(f"An error occurred: {err}")


@app.on_message(filters.command(["demote"], "."))
async def demoteFunc(client, message):
    try:
        if message.reply_to_message:
            user = message.reply_to_message.from_user.id
        elif not message.reply_to_message and len(message.command) != 1:
            user = message.text.split(None, 1)[1]
        else:
            await message.reply("Invalid command usage.")
            return

        umention = (await client.get_users(user)).mention
    except Exception:
        await message.reply("Invalid ID")
        return

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
        await message.reply("Successfully demoted.")
    except Exception as err:
        await message.reply(f"Error: {err}")