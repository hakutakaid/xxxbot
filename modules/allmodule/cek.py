from pyrogram import Client, filters
from modules.config import DEVS

@Client.on_message(filters.user(DEVS) & filters.command("cek", ""))
async def haku(client, message):
    await message.react(emoji="👻")