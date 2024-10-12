import asyncio
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired
from config import OWNER_ID
from AnonXMusic import app

# Function to check if the user is an administrator
async def is_administrator(user_id, chat_id, client):
    member = await client.get_chat_member(chat_id, user_id)
    return member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]

# Function to check if the user is the owner
async def is_owner(user_id):
    return user_id == OWNER_ID

@app.on_message(filters.command("kickall", prefixes=[".", "!", "/", ","]) & filters.group)
async def kick_all(client, message):
    kicked_count = 0
    admin = await is_administrator(message.from_user.id, message.chat.id, client)
    owner = await is_owner(message.from_user.id)

    # Check if the user has permission to kick members
    if not admin and not owner:
        return await message.reply("Sorry, you are not allowed to use this command!")

    response_message = await message.reply("Kicking all members...")

    # Check if the bot has permission to kick members
    bot_member = await client.get_chat_member(message.chat.id, client.me.id)
    if not bot_member.can_restrict_members:
        return await response_message.edit("Bot doesn't have permission to kick members.")

    async for user in client.get_chat_members(message.chat.id):
        if user.user.id != client.me.id:  # Skip the bot itself
            if not await is_administrator(user.user.id, message.chat.id, client) and not await is_owner(user.user.id):
                try:
                    # Kick the user (temporary removal)
                    await client.kick_chat_member(message.chat.id, user.user.id)
                    await asyncio.sleep(1)  # Wait a bit to avoid hitting API limits
                    kicked_count += 1
                except ChatAdminRequired:
                    return await response_message.edit("Bot doesn't have permission to kick members in this group.")
                except Exception as e:
                    # Log any other errors
                    print(f"Error while kicking {user.user.id}: {str(e)}")
                    continue

    final_count = len([user async for user in client.get_chat_members(message.chat.id)])
    del_status = f"Kicked {kicked_count} members" if kicked_count > 0 else "No members to kick."
    await response_message.edit(del_status)
    await asyncio.sleep(5)  # Wait 5 seconds before deleting the message
    await response_message.delete()