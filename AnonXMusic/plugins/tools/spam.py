from pyrogram import Client, filters
import asyncio

@app.on_message(filters.command(["spam"], prefixes=[".", "/"]) & filters.group)
async def spam(client, message):
    try:
        # Split the command text into components
        args = message.text.split()
        if len(args) < 3:
            await message.edit_text("Usage: .spam {reason} {number_of_messages}")
            return

        # Extract the number of messages from the last argument
        try:
            number_of_messages = int(args[-1])
        except ValueError:
            await message.edit_text("Please enter a valid number of messages.")
            return

        # Join the remaining arguments to form the reason
        reason = " ".join(args[1:-1])

        # Validate number of messages
        if number_of_messages <= 0:
            await message.edit_text("Number of messages must be greater than 0.")
            return

        # Delete the original command message
        await message.delete()

        # Send messages with a 2-second interval
        for _ in range(number_of_messages):
            await message.reply_text(reason)
            await asyncio.sleep(2)  # Sleep for 2 seconds asynchronously

    except Exception as e:
        await message.edit_text(f"An error occurred: {str(e)}")