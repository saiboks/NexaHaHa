import requests
from pyrogram import filters
from pyrogram.types import Message, ChatType
from AnonXMusic import app

@app.on_message(filters.command("cosplay"))
async def cosplay(_, msg):
    img = requests.get("https://waifu-api.vercel.app").json()
    await msg.reply_photo(img, caption="Here is your cosplay image!")

@app.on_message(filters.command("ncosplay"))
async def ncosplay(_, msg):
    if msg.chat.type != ChatType.PRIVATE:
        await msg.reply_text("❍ sᴏʀʀʏ ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ɪɴ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ ᴡɪᴛʜ ʙᴏᴛ")
    else:
        ncosplay = requests.get("https://waifu-api.vercel.app/items/1").json()
        await msg.reply_photo(ncosplay, caption="Here is your ncosplay image!")