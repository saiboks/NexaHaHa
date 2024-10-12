import asyncio
from pyrogram import Client, enums
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import OWNER_ID
from AnonXMusic import app


@app.on_message(filters.command("kickall", prefixes=[".", "!", "/", ","]) & filters.group)
async def kick_all(client, message):
    kicked_count = 0
    admin = await is_administrator(message.from_user.id, message, client)
    owner = await is_owner(message.from_user.id, message, client)

    if not admin or owner:
        return await message.edit("Sorry, you are not allowed to use this command!")  # Edit original message

    response_message = await message.edit("Kicking all members...")
    initial_count = len([user async for user in client.get_chat_members(message.chat.id)])

    async for user in client.get_chat_members(message.chat.id):
        if not await is_administrator(user.user.id, message, client) and not await is_owner(user.user.id, message, client):
            try:
                await client.ban_chat_member(message.chat.id, user.user.id)
                await client.unban_chat_member(message.chat.id, user.user.id)
                kicked_count += 1
            except ChatAdminRequired:
                return await response_message.edit("Do not have permission to kick in this group.")  # Edit original message

    final_count = len([user async for user in client.get_chat_members(message.chat.id)])
    del_status = f"Kicked {kicked_count} members" if kicked_count > 0 else "No members to kick."
    await response_message.edit(del_status)
    await forward_action_details(client, message, "Kick All", initial_count, final_count, kicked_count=kicked_count)
    await asyncio.sleep(5)  # Change to 5 seconds
    await response_message.delete()