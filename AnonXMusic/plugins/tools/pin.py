from pyrogram import filters
from pyrogram.types import Message

from AnonXMusic import app
from AnonXMusic.core.mongo import mongodb
from AnonXMusic.utils.database import save_filter
from AnonXMusic.utils.permissions import adminsOnly
from config import BANNED_USERS

# MongoDB collection
filtersdb = mongodb.filters  # Assuming this is your filters collection

# Function to get filters from the database
async def _get_filters(chat_id: int) -> dict:
    chat_filters = await filtersdb.find_one({"chat_id": chat_id})
    if not chat_filters:
        return {}  # Return an empty dictionary if no filters are found
    return chat_filters.get("filters", {})

# Function to save filters to the database
async def save_filter(chat_id: int, name: str, _filter: dict):
    name = name.lower().strip()
    _filters = await _get_filters(chat_id)
    _filters[name] = _filter
    await filtersdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"filters": _filters}},
        upsert=True,
    )

# pin/unpin command handler
@app.on_message(filters.command(["pin", "unpin"]) & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_pin_messages")
async def pin(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a message to pin/unpin it.")

    r = message.reply_to_message
    if message.command[0][0] == "u":  # For "unpin"
        await r.unpin()
        return await message.reply_text(
            f"Unpinned [this](t.me/c/{r.chat.id}/{r.id}) message.",
            disable_web_page_preview=True,
        )

    # For "pin"
    await r.pin(disable_notification=True)
    await message.reply_text(
        f"Pinned [this](t.me/c/{r.chat.id}/{r.id}) message.",
        disable_web_page_preview=True,
    )

    # Save the pin as a filter
    msg = "Please check the pinned message: ~ " + f"[Check, t.me/c/{r.chat.id}/{r.id}]"
    filter_ = dict(type="text", data=msg)
    await save_filter(message.chat.id, "~pinned", filter_)