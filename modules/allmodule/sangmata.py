#izzy

import asyncio
from pyrogram import Client
from pyrogram.errors import YouBlockedUser
from pyrogram.types import Message
from pyrogram import filters
from pyrogram.errors import YouBlockedUser
from pyrogram.raw.functions.messages import DeleteHistory
from helper.misc import *
from modules.config import cmd

# ... (previous code) ...

@Client.on_message(filters.me & filters.command("sg", cmd))
async def sg(client: Client, message: Message):
    args = await extract_user(message)
    lol = await message.edit_text("`Processing...`")
    user = None  # Initialize the 'user' variable with None
    if args:
        try:
            user = await client.get_users(args)
        except Exception:
            return await lol.edit(f"`Please specify a valid user!`")
    bot = "SangMata_beta_bot"
    bot_info = await client.resolve_peer("SangMata_beta_bot")
    try:
        if user:  # Check if 'user' is not None before using it
            await client.send_message(bot, f"{user.id}")
        else:
            return await lol.edit(f"`User not found or invalid!`")
    except YouBlockedUser:
        await client.unblock_user(bot)
        if user:  # Check if 'user' is not None before using it
            await client.send_message(bot, f"{user.id}")
        else:
            return await lol.edit(f"`User not found or invalid!`")
    await asyncio.sleep(1)

    async for stalk in client.search_messages(bot, query="Name", limit=1):
        if not stalk:
            await message.edit_text("**Orang Ini Belum Pernah Mengganti Namanya**")
            return
        elif stalk:
            await message.edit(stalk.text)
            await stalk.delete()
    async for stalk in client.search_messages(bot, query="Username", limit=1):
        if not stalk:
            return
        elif stalk:
            await message.edit(stalk.text)
            await stalk.delete()
    return await client.invoke(DeleteHistory(peer=bot_info, max_id=0, revoke=True))