import time
from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

import config
from AnonXMusic import app
from AnonXMusic.misc import _boot_
from AnonXMusic.plugins.sudo.sudoers import sudoers_list
from AnonXMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from AnonXMusic.utils.decorators.language import LanguageStart
from AnonXMusic.utils.formatters import get_readable_time
from AnonXMusic.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string

# Initialize Pyrogram Client
app = Client("my_bot")

@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    if len(message.text.split()) > 1:
        # Handle other commands like help, sudo, etc.
        pass
    else:
        try:
            # Fetch profile photo of the user
            profile_photos = await client.get_profile_photos(message.from_user.id)
            if profile_photos.total_count > 0:
                # Use the first profile photo
                photo = profile_photos.photos[0][0].file_id
            else:
                # Default image if no profile picture
                photo = config.START_IMG_URL
        except Exception as e:
            # Log the error and use default image in case of any error
            print(f"Failed to get profile photos: {e}")
            photo = config.START_IMG_URL

        # Create the panel for the start message
        out = private_panel(_)
        await message.reply_photo(
            photo=photo,
            caption=_["start_2"].format(message.from_user.mention, client.mention),
        )

        await message.reply_text(
            text=_["start_3"].format(client.mention),
            reply_markup=InlineKeyboardMarkup(out),
        )

        # Check if logging is enabled
        if await is_on_off(2):
            await client.send_message(
                chat_id=config.LOGGER_ID,
                text=f"{message.from_user.mention} just started the bot.\n\n"
                     f"<b>User ID:</b> <code>{message.from_user.id}</code>\n"
                     f"<b>Username:</b> @{message.from_user.username}",
            )

# Start bot in group chat
@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)

# Handle new chat members
@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass
            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_5"])
                    return await app.leave_chat(message.chat.id)
                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_6"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)
                await message.reply_photo(
                    photo=config.START_IMG_URL,
                    caption=_["start_4"].format(
                        message.from_user.first_name,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(ex)