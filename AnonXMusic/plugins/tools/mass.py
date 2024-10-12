import config
from AnonXMusic import app
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions, CallbackQuery
from pyrogram.enums import ChatMemberStatus


# Mute All command
@app.on_message(filters.command(["muteall"], prefixes=["/", "!", ".", ","]))
async def mute_all_users(client, message):
    chat_id = message.chat.id
    issuer = message.from_user  # The user issuing the mute command

    # Ensure the user issuing the command has ban rights
    issuer_member = await client.get_chat_member(chat_id, issuer.id)
    if issuer_member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER] or not issuer_member.privileges.can_restrict_members:
        await message.reply_text("You don't have permission to mute users.")
        return

    bot = await client.get_chat_member(chat_id, client.me.id)
    if not bot.privileges.can_restrict_members:
        await message.reply_text("I don't have the permission to mute users.")
        return

    muted_count = 0  # To track how many members are muted

    async for member in client.get_chat_members(chat_id):
        if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            try:
                # Mute the user (restrict sending messages)
                await client.restrict_chat_member(
                    chat_id,
                    member.user.id,
                    permissions=ChatPermissions(can_send_messages=False)
                )
                muted_count += 1  # Increment counter for each successfully muted member
            except Exception as e:
                await message.reply_text(f"Failed to mute {member.user.first_name}: {str(e)}")

    await message.reply_text(f"Muted {muted_count} non-admin members successfully.")


# Unmute All command
@app.on_message(filters.command(["unmuteall"], prefixes=["/", "!", ".", ","]))
async def unmute_all_users(client, message):
    chat_id = message.chat.id
    issuer = message.from_user  # The user issuing the unmute command

    # Ensure the user issuing the command has ban rights
    issuer_member = await client.get_chat_member(chat_id, issuer.id)
    if issuer_member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER] or not issuer_member.privileges.can_restrict_members:
        await message.reply_text("You don't have permission to unmute users.")
        return

    bot = await client.get_chat_member(chat_id, client.me.id)
    if not bot.privileges.can_restrict_members:
        await message.reply_text("I don't have the permission to unmute users.")
        return

    unmuted_count = 0  # To track how many members are unmuted

    async for member in client.get_chat_members(chat_id):
        if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            try:
                # Unmute the user (restore permissions)
                await client.restrict_chat_member(
                    chat_id,
                    member.user.id,
                    permissions=ChatPermissions(
                        can_send_messages=True,
                        can_send_media_messages=True,
                        can_send_polls=True,
                        can_add_web_page_previews=True,
                        can_change_info=True,
                        can_invite_users=True,
                        can_pin_messages=True
                    )
                )
                unmuted_count += 1  # Increment counter for each successfully unmuted member
            except Exception as e:
                await message.reply_text(f"Failed to unmute {member.user.first_name}: {str(e)}")

    await message.reply_text(f"Unmuted {unmuted_count} non-admin members successfully.")