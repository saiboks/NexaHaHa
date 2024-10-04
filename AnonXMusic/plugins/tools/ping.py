from datetime import datetime
from pyrogram import filters
from pyrogram.types import Message

from AnonXMusic import app
from AnonXMusic.core.call import Anony
from AnonXMusic.utils import bot_sys_stats
from AnonXMusic.utils.decorators.language import language
from AnonXMusic.utils.inline import supp_markup
from config import BANNED_USERS, PING_IMG_URL


@app.on_message(filters.command(["ping", "alive"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    start = datetime.now()

    # Pehle image ke saath reply karo
    response = await message.reply_photo(
        photo=PING_IMG_URL,
        caption="{0} ɪs ᴘɪɴɢɪɴɢ...".format(app.mention),  # App mention will replace {0}
    )

    # Ping aur system stats calculate karo
    pytgping = await Anony.ping()  # Checking Py-TGCalls ping
    UP, CPU, RAM, DISK = await bot_sys_stats()  # Fetch system stats
    resp = (datetime.now() - start).microseconds / 1000  # Time calculation

    # Image ko delete karo
    await response.delete()

    # Stats ke saath reply karo
    await message.reply_text(
        _["ping_2"].format(resp, app.mention, UP, RAM, CPU, DISK, pytgping),  # Formatting stats
        reply_markup=supp_markup(_),  # Optional button markup
    )