import asyncio 
from pyrogram import Client, filters
from pyrogram.types import Message
from modules.config import cmd

def get_user(message: Message, text: str) -> [int, str, None]:
    """Get User From Message"""
    if text is None:
        asplit = None
    else:
        asplit = text.split(" ", 1)
    user_s = None
    reason_ = None
    if message.reply_to_message:
        user_s = message.reply_to_message.from_user.id
        reason_ = text if text else None
    elif asplit is None:
        return None, None
    elif len(asplit[0]) > 0:
        if message.entities:
            if len(message.entities) == 1:
                required_entity = message.entities[0]
                if required_entity.type == "text_mention":
                    user_s = int(required_entity.user.id)
                else:
                    user_s = int(asplit[0]) if asplit[0].isdigit() else asplit[0]
        else:
            user_s = int(asplit[0]) if asplit[0].isdigit() else asplit[0]
        if len(asplit) == 2:
            reason_ = asplit[1]
    return user_s, reason_


async def edit_or_reply(message: Message, *args, **kwargs) -> Message:
    apa = (
        message.edit_text
        if bool(message.from_user and message.from_user.is_self or message.outgoing)
        else (message.reply_to_message or message).reply_text
    )
    return await apa(*args, **kwargs)


eor = edit_or_reply


@Client.on_message(filters.me & filters.command("purgeme", cmd)) 
async def purge_me_func(client, message): 
     if len(message.command) != 2: 
         return await message.delete() 
     n = ( 
         message.reply_to_message 
         if message.reply_to_message 
         else message.text.split(None, 1)[1].strip() 
     ) 
     if not n.isnumeric(): 
         return await eor(message, "Argumen Tidak Valid") 
     n = int(n) 
     if n < 1: 
         return await eor(message, "Butuh nomor >=1-999") 
     chat_id = message.chat.id 
     message_ids = [ 
         m.id 
         async for m in client.search_messages( 
             chat_id, 
             from_user=int(message.from_user.id), 
             limit=n, 
         ) 
     ] 
     if not message_ids: 
         return await eor(message, text="Tidak ada pesan yang ditemukan.") 
     to_delete = [message_ids[i : i + 999] for i in range(0, len(message_ids), 999)] 
     for hundred_messages_or_less in to_delete: 
         await client.delete_messages( 
             chat_id=chat_id, 
             message_ids=hundred_messages_or_less, 
             revoke=True, 
         ) 
         mmk = await eor(message, f"✅ {n} Pesan Telah Di Hapus") 
         await asyncio.sleep(2) 
         await mmk.delete()