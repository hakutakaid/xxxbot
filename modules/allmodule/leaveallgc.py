from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import *
from modules.config import dontleave, cmd

@Client.on_message(filters.command("lagc", cmd) & filters.me)
async def kickmeall(client, message):
    tex = await message.reply_text("`Global Leave from group chats...`")
    er = 0
    done = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            chat = dialog.chat.id
            if chat not in dontleave:
                try:
                    done += 1
                    await client.leave_chat(chat)
                except BaseException:
                    er += 1
    await tex.edit(f"**Successfully left {done} Groups, Failed to left {er} Groups**")
