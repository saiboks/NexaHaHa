import random
import time
import requests
from AnonXMusic import app
from config import BOT_USERNAME

from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters

# Importing TheApi instead of ChatGPT API
from TheApi import api

@app.on_message(filters.command(["chatgpt", "ai", "ask", "gpt", "solve"], prefixes=["+", ".", "/", "-", "", "$", "#", "&"]))
async def chat_gpt(bot, message):
    try:
        start_time = time.time()
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

        if len(message.command) < 2:
            await message.reply_text(
                "**⬤ ᴇxᴀᴍᴘʟᴇ ➠** `/ask Where is TajMahal ?`"
            )
        else:
            question = message.text.split(' ', 1)[1]

            # Using TheApi's `chatgpt()` method to get the response
            response = api.chatgpt(question)

            # Fetching bot's name using get_me()
            bot_info = await bot.get_me()
            bot_name = bot_info.first_name
            bot_id = bot_info.id

            # Assuming `response` is directly the answer or response in a string format
            if response:
                end_time = time.time()
                telegram_ping = str(round((end_time - start_time) * 1000, 3)) + " ms"
                await message.reply_text(
                    f"🪐 {response.strip()}  \n\n**⬤ ᴀɴsᴡᴇʀɪɴɢ ʙʏ ➠ [{bot_name}](tg://user?id={bot_id})**",
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await message.reply_text("No answer found in the response.")
    except Exception as e:
        await message.reply_text(f"Error - {e}")