import asyncio
from pyrogram import Client, enums
from pyrogram import filters
from pyrogram.errors import ChatAdminRequired
from config import OWNER_ID
from AnonXMusic import app

# Check if user is admin
async def is_administrator(user_id, message, client):
    member = await client.get_chat_member(message.chat.id, user_id)
    return member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]

# Check if user is owner
async def is_owner(user_id, message, client):
    return user_id == OWNER_ID

@app.on_message(filters.command("kickall", prefixes=[".", "!", "/", ","]) & filters.group)
async def kick_all(client, message):
    kicked_count = 0
    admin = await is_administrator(message.from_user.id, message, client)
    owner = await is_owner(message.from_user.id, message, client)

    if not admin and not owner:
        return await message.reply("Sorry, you are not allowed to use this command!")  # Use reply instead of edit

    response_message = await message.reply("Kicking all members...")
    initial_count = len([user async for user in client.get_chat_members(message.chat.id)])

    async for user in client.get_chat_members(message.chat.id):
        if not await is_administrator(user.user.id, message, client) and not await is_owner(user.user.id, message, client):
            try:
                # Kick the user (temporary removal)
                await client.kick_chat_member(message.chat.id, user.user.id)
                kicked_count += 1
            except ChatAdminRequired:
                return await response_message.edit("Bot doesn't have permission to kick members in this group.")  # Edit response

    final_count = len([user async for user in client.get_chat_members(message.chat.id)])
    del_status = f"Kicked {kicked_count} members" if kicked_count > 0 else "No members to kick."
    await response_message.edit(del_status)
    await asyncio.sleep(5)  # Wait 5 seconds before deleting
    await response_message.delete()