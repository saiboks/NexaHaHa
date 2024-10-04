from pyrogram import Client, filters
from pyrogram.types import Message
from AnonXMusic import app

# Command to get group information based on username
@app.on_message(filters.command("groupinfo", prefixes="/"))
async def get_group_status(_, message: Message):
    if len(message.command) != 2:
        await message.reply("Please provide a group username. Example: `/groupinfo YourGroupUsername`")
        return

    group_username = message.command[1]

    try:
        group = await app.get_chat(group_username)
    except Exception as e:
        await message.reply(f"Error: {e}")
        return

    total_members = await app.get_chat_members_count(group.id)
    group_description = group.description
    premium_acc = banned = deleted_acc = bot = 0  # You should replace these variables with actual counts.

    response_text = (
        f"<b><u>⬤ ɢʀᴏᴜᴘ ɪɴғᴏʀᴍᴀᴛɪᴏɴ </u>𐏓</b>\n\n"
        f"<b>● ɢʀᴏᴜᴘ ɴᴀᴍᴇ ➠</b> {group.title}\n"
        f"<b>● ɢʀᴏᴜᴘ ɪᴅ ➠</b> {group.id}\n"
        f"<b>● ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀs ➠</b> {total_members}\n"
        f"<b>● ᴜsᴇʀɴᴀᴍᴇ ➠</b> @{group_username}\n"
        f"<b>● ᴅᴇsᴄʀɪᴘᴛɪᴏɴ ➠</b> \n{group_description or 'N/A'}"
    )

    await message.reply(response_text)


# Command to get the status of the current group
@app.on_message(filters.command("status") & filters.group)
async def group_status(client, message: Message):
    chat = message.chat  # Chat where the command was sent
    status_text = (
        f"<b>● ɢʀᴏᴜᴘ ɪᴅ ➠</b> {chat.id}\n"
        f"<b>● ᴛɪᴛʟᴇ ➠</b> {chat.title}\n"
        f"<b>● ᴛʏᴘᴇ ➠</b> {chat.type}\n"
    )

    if chat.username:  # Not all groups have a username
        status_text += f"<b>● ᴜsᴇʀɴᴀᴍᴇ ➠</b> @{chat.username}\n"
    else:
        status_text += "<b>● ᴜsᴇʀɴᴀᴍᴇ ➠</b> None\n"

    await message.reply_text(status_text)


# Running the bot
if __name__ == "__main__":
    app.run()