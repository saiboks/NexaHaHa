from traceback import format_exc
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from search_engine_parser.core.engines.google import Search as GoogleSearch
from search_engine_parser.core.engines.stackoverflow import \
    Search as StackSearch
from search_engine_parser.core.exceptions import NoResultsFound, NoResultsOrTrafficError
from AnonXMusic import app
from pyrogram import filters




gsearch = GoogleSearch()
stsearch = StackSearch()



def ikb(rows=None, back=False, todo="start_back"):
    """
    rows = pass the rows
    back - if want to make back button
    todo - callback data of back button
    """
    if rows is None:
        rows = []
    lines = []
    try:
        for row in rows:
            line = []
            for button in row:
                btn_text = button.split(".")[1].capitalize()
                button = btn(btn_text, button)  
                line.append(button)
            lines.append(line)
    except AttributeError:
        for row in rows:
            line = []
            for button in row:
                button = btn(*button)  
                line.append(button)
            lines.append(line)
    except TypeError:
        # make a code to handel that error
        line = []
        for button in rows:
            button = btn(*button)  # InlineKeyboardButton
            line.append(button)
        lines.append(line)
    if back: 
        back_btn = [(btn("ʙᴀᴄᴋ", todo))]
        lines.append(back_btn)
    return InlineKeyboardMarkup(inline_keyboard=lines)


def btn(text, value, type="callback_data"):
    return InlineKeyboardButton(text, **{type: value})


# ------------------------------------------------------------------------------- #



@app.on_message(filters.command('google'))
async def search_(app: app, msg: Message):
    split = msg.text.split(None, 1)
    if len(split) == 1:
        return await msg.reply_text("⬤ ɢɪᴠᴇ ǫᴜᴇʀʏ ᴛᴏ sᴇᴀʀᴄʜ.")
    to_del = await msg.reply_text("🔍")
    query = split[1]
    try:
        result = await gsearch.async_search(query)
        keyboard = ikb(
            [
                [
                    (
                        f"{result[0]['titles']}",
                        f"{result[0]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[1]['titles']}",
                        f"{result[1]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[2]['titles']}",
                        f"{result[2]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[3]['titles']}",
                        f"{result[3]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[4]['titles']}",
                        f"{result[4]['links']}",
                        "url",
                    ),
                ],
            ]
        )

        txt = f"⬤ ʜᴇʀᴇ ᴀʀᴇ ᴛʜᴇ ʀᴇsᴜʟᴛs ᴏғ ʀǫᴜᴇsᴛᴇᴅ ➥ {query.title()}"
        await to_del.delete()
        await msg.reply_text(txt, reply_markup=keyboard)
        return
    except NoResultsFound:
        await to_del.delete()
        await msg.reply_text("⬤ ɴᴏ ʀᴇsᴜʟᴛ ғᴏᴜɴᴅ ᴄᴏʀʀᴇsᴘᴏɴᴅɪɴɢ ᴛᴏ ʏᴏᴜʀ ǫᴜᴇʀʏ.")
        return
    except NoResultsOrTrafficError:
        await to_del.delete()
        await msg.reply_text("⬤ ɴᴏ ʀᴇsᴜʟᴛ ғᴏᴜɴᴅ ᴅᴜᴇ ᴛᴏ ᴛᴏᴏ ᴍᴀɴʏ ᴛʀᴀғғɪᴄ.")
        return
    except Exception as e:
        await to_del.delete()
        await msg.reply_text(f"⬤ sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ ➥ ʀᴇᴘᴏʀᴛ ᴀᴛ ɪᴛ.")
        print(f"error : {e}")
        return


# ------------------------------------------------------------------------------- #



@app.on_message(filters.command('stack'))
async def stack_search_(app: app, msg: Message):
    split = msg.text.split(None, 1)
    if len(split) == 1:
        return await msg.reply_text("⬤ ɢɪᴠᴇ ǫᴜᴇʀʏ ᴛᴏ sᴇᴀʀᴄʜ.")
    to_del = await msg.reply_text("🔍")
    query = split[1]
    try:
        result = await stsearch.async_search(query)
        keyboard = ikb(
            [
                [
                    (
                        f"{result[0]['titles']}",
                        f"{result[0]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[1]['titles']}",
                        f"{result[1]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[2]['titles']}",
                        f"{result[2]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[3]['titles']}",
                        f"{result[3]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[4]['titles']}",
                        f"{result[4]['links']}",
                        "url",
                    ),
                ],
            ]
        )

        txt = f"⬤ ʜᴇʀᴇ ᴀʀᴇ ᴛʜᴇ ʀᴇsᴜʟᴛs ᴏғ ʀǫᴜᴇsᴛᴇᴅ ➥ {query.title()}"
        await to_del.delete()
        await msg.reply_text(txt, reply_markup=keyboard)
        return
    except NoResultsFound:
        await to_del.delete()
        await msg.reply_text("⬤ ɴᴏ ʀᴇsᴜʟᴛ ғᴏᴜɴᴅ ᴄᴏʀʀᴇsᴘᴏɴᴅɪɴɢ ᴛᴏ ʏᴏᴜʀ ǫᴜᴇʀʏ.")
        return
    except NoResultsOrTrafficError:
        await to_del.delete()
        await msg.reply_text("⬤ ɴᴏ ʀᴇsᴜʟᴛ ғᴏᴜɴᴅ ᴅᴜᴇ ᴛᴏ ᴛᴏᴏ ᴍᴀɴʏ ᴛʀᴀғғɪᴄ.")
        return
    except Exception as e:
        await to_del.delete()
        await msg.reply_text(f"⬤ sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ ➥ ʀᴇᴘᴏʀᴛ ᴀᴛ ɪᴛ.")
        print(f"⬤ error ➥ {e}")
        return




# ------------------------------------------------------------------------------- #



from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from search_engine_parser.core.engines.duckduckgo import Search as DuckSearch
from AnonXMusic import app  # Bot's core module

import re  # To validate URLs

# Initialize DuckDuckGo Search
dsearch = DuckSearch()

# Function to validate URL
def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
        r'?[A-F0-9]*:[A-F0-9:]+?)' # ...or ipv6
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

@app.on_message(filters.command('duck'))
async def duck_search_(app: app, msg: Message):
    # Extract query from the message
    split = msg.text.split(None, 1)
    if len(split) == 1:
        return await msg.reply_text("⬤ Please provide a query to search.")
    
    to_del = await msg.reply_text("🔍 Searching DuckDuckGo...")
    query = split[1]

    try:
        # Perform the search and fetch the result
        result = await dsearch.async_search(query, 1)  # Fetch top search results
        
        # Extract titles and links from the result
        titles, links = result['titles'], result['links']

        # Check if results exist
        if not titles or not links:
            await to_del.delete()
            return await msg.reply_text("⬤ No results found for your query.")
        
        # Prepare the keyboard with valid URLs
        keyboard = []
        for i in range(min(3, len(titles))):  # Limit to top 3 results
            url = links[i]
            if is_valid_url(url):  # Only add buttons with valid URLs
                keyboard.append([InlineKeyboardButton(titles[i], url=url)])

        # Check if keyboard has valid buttons
        if not keyboard:
            await to_del.delete()
            return await msg.reply_text("⬤ No valid URLs found for the query.")

        # Create an InlineKeyboardMarkup object
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Format the response text
        txt = f"⬤ Here are the top results for ➥ {query.title()}:"

        # Send the results back to the user
        await to_del.delete()
        await msg.reply_text(txt, reply_markup=reply_markup)
        return

    except Exception as e:
        # Handle exceptions if something goes wrong
        await to_del.delete()
        await msg.reply_text(f"⬤ Something went wrong ➥ {e}")
        return