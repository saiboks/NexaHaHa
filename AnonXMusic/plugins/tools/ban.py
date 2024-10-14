@app.on_message(filters.command(["kick", "skick"]) & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_restrict_members")
async def kickFunc(_, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    
    if not user_id:
        return await message.reply_text("ɪ ᴄᴀɴ'ᴛ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ")
    if user_id == app.id:
        return await message.reply_text("ɪ ᴄᴀɴ'ᴛ ᴋɪᴄᴋ ᴍʏsᴇʟғ, ɪ ᴄᴀɴ ʟᴇᴀᴠᴇ ɪғ ʏᴏᴜ ᴡᴀɴᴛ.")
    if user_id in SUDOERS:
        return await message.reply_text("ʏᴏᴜ ᴡᴀɴɴᴀ ᴋɪᴄᴋ ᴛʜᴇ ᴇʟᴇᴠᴀᴛᴇᴅ ᴏɴᴇ ?")
    if user_id in [
        member.user.id
        async for member in app.get_chat_members(
            chat_id=message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]:
        return await message.reply_text("ɪ ᴄᴀɴ'ᴛ ᴋɪᴄᴋ ᴀɴ ᴀᴅᴍɪɴ, ʏᴏᴜ ᴋɴᴏᴡ ᴛʜᴇ ʀᴜʟᴇs.")
    
    # Kick the user
    await message.chat.ban_member(user_id)
    
    # Create the mention string and kick reason
    mention = (await app.get_users(user_id)).mention
    msg = f"<b>{mention} ᴋɪᴄᴋᴇᴅ ғʀᴏᴍ ᴛʜᴇ ᴄʜᴀᴛ.</b>"
    
    # Send the kick message
    kick_message = await message.reply_text(msg)
    
    # Unban the user to allow them to join back later
    await asyncio.sleep(1)
    await message.chat.unban_member(user_id)
    
    # Delete the command message and related replies (if applicable)
    await message.delete()
    if message.reply_to_message:
        await message.reply_to_message.delete()
    
    # Optionally delete the kick notification after a few seconds (clean up)
    await asyncio.sleep(5)
    await kick_message.delete()

    # Delete user history if 's' command was used
    if message.command[0][0] == "s":
        await app.delete_user_history(message.chat.id, user_id)