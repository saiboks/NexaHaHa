import config
from config import OWNER_ID
from AnonXMusic import app
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions, CallbackQuery
from pyrogram.enums import ChatMemberStatus


# Mute All command
@app.on_message(filters.command(["muteall"], prefixes=["/", "!", ".", ","]))
async def mute_all_users(client, message):
    chat_id = message.chat.id
    issuer = message.from_user  # The user issuing the mute command

    # Ensure the user issuing the command is either the bot owner or the group owner
    if issuer.id != OWNER_ID:
        issuer_member = await client.get_chat_member(chat_id, issuer.id)
        if issuer_member.status != ChatMemberStatus.OWNER:
            await message.reply_text("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ. ᴏɴʟʏ ᴛʜᴇ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs.")
            return

    # Send confirmation message with buttons
    buttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("Approve", callback_data="approve_mute"),
            InlineKeyboardButton("Decline", callback_data="decline_mute")
        ]]
    )
    await message.reply_text("Do you really want to mute all members?", reply_markup=buttons)


# Callback for Mute All Approval
@app.on_callback_query(filters.regex("approve_mute"))
async def approve_mute(client, callback_query: CallbackQuery):
    message = callback_query.message
    chat_id = message.chat.id

    # Check if user has the right to approve
    issuer = callback_query.from_user
    if issuer.id != OWNER_ID:
        issuer_member = await client.get_chat_member(chat_id, issuer.id)
        if issuer_member.status != ChatMemberStatus.OWNER:
            await callback_query.answer("Only the bot owner or the group owner can approve this.", show_alert=True)
            return

    # Mute all non-admin members
    bot = await client.get_chat_member(chat_id, client.me.id)
    if not bot.privileges.can_restrict_members:
        await message.edit_text("I don't have the permission to mute users.")
        return

    starting_message = await message.edit_text("ᴍᴜᴛᴇᴀʟʟ sᴛᴀʀᴛɪɴɢ . . .")
    muted_count = 0

    async for member in client.get_chat_members(chat_id):
        if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER] and member.user.id != OWNER_ID:
            try:
                await client.restrict_chat_member(
                    chat_id,
                    member.user.id,
                    permissions=ChatPermissions(can_send_messages=False)
                )
                muted_count += 1
            except Exception as e:
                await message.reply_text(f"Failed to mute {member.user.first_name}: {str(e)}")

    await starting_message.edit_text(f"Muted {muted_count} non-admin members successfully.")
    await callback_query.answer()


# Callback for Decline
@app.on_callback_query(filters.regex("decline_mute"))
async def decline_mute(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text("Mute operation has been declined.")
    await callback_query.answer()


# Unmute All command
@app.on_message(filters.command(["unmuteall"], prefixes=["/", "!", ".", ","]))
async def unmute_all_users(client, message):
    chat_id = message.chat.id
    issuer = message.from_user  # The user issuing the unmute command

    # Ensure the user issuing the command is either the bot owner or the group owner
    if issuer.id != OWNER_ID:
        issuer_member = await client.get_chat_member(chat_id, issuer.id)
        if issuer_member.status != ChatMemberStatus.OWNER:
            await message.reply_text("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ. ᴏɴʟʏ ᴛʜᴇ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs.")
            return

    # Send confirmation message with buttons
    buttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("Approve", callback_data="approve_unmute"),
            InlineKeyboardButton("Decline", callback_data="decline_unmute")
        ]]
    )
    await message.reply_text("Do you really want to unmute all members?", reply_markup=buttons)


# Callback for Unmute All Approval
@app.on_callback_query(filters.regex("approve_unmute"))
async def approve_unmute(client, callback_query: CallbackQuery):
    message = callback_query.message
    chat_id = message.chat.id

    # Check if user has the right to approve
    issuer = callback_query.from_user
    if issuer.id != OWNER_ID:
        issuer_member = await client.get_chat_member(chat_id, issuer.id)
        if issuer_member.status != ChatMemberStatus.OWNER:
            await callback_query.answer("ᴏɴʟʏ ᴛʜᴇ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ ᴄᴀɴ ᴀᴘᴘʀᴏᴠᴇ ᴛʜɪs.", show_alert=True)
            return

    # Unmute all non-admin members
    bot = await client.get_chat_member(chat_id, client.me.id)
    if not bot.privileges.can_restrict_members:
        await message.edit_text("I don't have the permission to unmute users.")
        return

    starting_message = await message.edit_text("ᴜɴᴍᴜᴛᴇᴀʟʟ sᴛᴀʀᴛɪɴɢ . . .")
    unmuted_count = 0

    async for member in client.get_chat_members(chat_id):
        if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            try:
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
                unmuted_count += 1
            except Exception as e:
                await message.reply_text(f"Failed to unmute {member.user.first_name}: {str(e)}")

    await starting_message.edit_text(f"Unmuted {unmuted_count} non-admin members successfully.")
    await callback_query.answer()


# Callback for Decline
@app.on_callback_query(filters.regex("decline_unmute"))
async def decline_unmute(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text("Unmute operation has been declined.")
    await callback_query.answer()