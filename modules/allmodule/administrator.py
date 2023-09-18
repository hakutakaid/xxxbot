"""
• • • • • • • • • • • • • • • • • • • • • • • •
• Created By hakutakaid@github.com •
• Thanks To Pyroman-Userbot • 
• Thanks To Naya-Pyro •
• Thanks To Zaid-Userbot •
• • • • • • • • • • • • • • • • • • •• • • • • •
"""
import asyncio

from helper import *
from modules.config import cmd, DEVS
import time
from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import ChatPermissions, ChatPrivileges, Message
from helper.misc import *

unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)


@Client.on_message(filters.me & filters.command(["setgpic"], cmd))
async def set_chat_photo(client: Client, message: Message):
    chat_member = await client.get_chat_member(message.chat.id, client.me.id)
    
    if chat_member is None:
        return await eor(message, f"Failed to retrieve chat member information.")
    
    privileges = chat_member.privileges
    
    if privileges is None or not privileges.can_change_info:
        return await eor(message, f"You are not an admin in {message.chat.title}")
    
    if message.reply_to_message and message.reply_to_message.photo:
        await client.set_chat_photo(
            message.chat.id, photo=message.reply_to_message.photo.file_id
        )
    else:
        await eor(message, "Reply to a photo to set it as the group photo.")


@Client.on_message(filters.command(["ban", "dban"], cmd) & filters.me)
async def member_ban(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    ky = await eor(message, "`Processing...`")
    if not user_id:
        return await ky.edit("Tidak dapat menemukan pengguna.")
    if user_id == client.me.id:
        return await ky.edit("Tidak bisa banned diri sendiri.")
    if user_id in DEVS:
        return await ky.edit("Tidak bisa banned Devs!")
    if user_id in (await list_admins(client, message.chat.id)):
        return await ky.edit("Tidak bisa banned admin.")
    try:
        # await ky.delete()
        mention = (await client.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    msg = f"<b>Banned User:</b> {mention}\n<b>Banned By:</b> {message.from_user.mention}\n"
    if reason:
        msg += f"<b>Reason:</b> {reason}"
    try:
        await message.chat.ban_member(user_id)
        await ky.edit(msg)
    except ChatAdminRequired:
        return await ky.edit("**Anda bukan admin di group ini !**")


@Client.on_message(filters.command(["unban"], cmd) & filters.me)
async def member_unban(client: Client, message: Message):
    reply = message.reply_to_message
    zz = await eor(message, "`Processing...`")
    if reply and reply.sender_chat and reply.sender_chat != message.chat.id:
        return await zz.edit("`Tidak bisa unban ch`")

    if len(message.command) == 2:
        user = message.text.split(None, 1)[1]
    elif len(message.command) == 1 and reply:
        user = message.reply_to_message.from_user.id
    else:
        return await zz.edit("Berikan username, atau reply pesannya.")
    try:
        await message.chat.unban_member(user)
        await asyncio.sleep(0.1)
        # await zz.delete()
        umention = (await client.get_users(user)).mention
        await zz.edit(f"Unbanned! {umention}")
    except ChatAdminRequired:
        return await zz.edit("**Anda bukan admin di group ini !**")


@Client.on_message(filters.command(["pin", "unpin"], cmd) & filters.me)
async def pin_message(client: Client, message):
    if not message.reply_to_message:
        return await eor(message, "Balas ke pesan untuk pin/unpin .")
    await eor(message, "`Processing...`")
    r = message.reply_to_message
    if message.command[0][0] == "u":
        await r.unpin()
        return await eor(
            message,
            f"**Unpinned [this]({r.link}) message.**",
            disable_web_page_preview=True,
        )
    try:
        await r.pin(disable_notification=True)
        await eor(
            message,
            f"**Pinned [this]({r.link}) message.**",
            disable_web_page_preview=True,
        )
    except ChatAdminRequired:
        return await eor(message, "**Anda bukan admin di group ini !**")


@Client.on_message(filters.command(["mute"], cmd) & filters.me)
async def mute(client, message):
    user_id, reason = await extract_user_and_reason(message)
    nay = await eor(message, "`Processing...`")
    if not user_id:
        return await nay.edit("Pengguna tidak ditemukan.")
    if user_id == client.me.id:
        return await nay.edit("Tidak bisa mute diri sendiri.")
    if user_id in DEVS:
        return await nay.edit("Tidak bisa mute dev!")
    if user_id in (await list_admins(client, message.chat.id)):
        return await nay.edit("Tidak bisa mute admin.")
    # await nay.delete()
    mention = (await client.get_users(user_id)).mention
    msg = (
        f"**Muted User:** {mention}\n"
        f"**Muted By:** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if reason:
        msg += f"**Reason:** {reason}"
    try:
        await message.chat.restrict_member(user_id, permissions=ChatPermissions())
        await nay.edit(msg)
    except ChatAdminRequired:
        return await nay.edit("**Anda bukan admin di group ini !**")


@Client.on_message(filters.command(["unmute"], cmd) & filters.me)
async def unmute(client: Client, message: Message):
    user_id = await extract_user(message)
    kl = await eor(message, "`Processing...`")
    if not user_id:
        return await kl.edit("Pengguna tidak ditemukan.")
    try:
        await message.chat.restrict_member(user_id, permissions=unmute_permissions)
        # await kl.delete()
        umention = (await client.get_users(user_id)).mention
        await kl.edit(f"Unmuted! {umention}")
    except ChatAdminRequired:
        return await kl.edit("**Anda bukan admin di group ini !**")


@Client.on_message(filters.command(["kick", "dkick"], cmd) & filters.me)
async def kick_user(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    ny = await eor(message, "`Processing...`")
    if not user_id:
        return await ny.edit("Pengguna tidak ditemukan.")
    if user_id == client.me.id:
        return await ny.edit("Tidak bisa kick diri sendiri.")
    if user_id == DEVS:
        return await ny.edit("Tidak bisa kick dev!.")
    if user_id in (await list_admins(client, message.chat.id)):
        return await ny.edit("Tidak bisa kick admin.")
    # await ny.delete()
    mention = (await client.get_users(user_id)).mention
    msg = f"""
**Kicked User:** {mention}
**Kicked By:** {message.from_user.mention if message.from_user else 'Anon'}"""
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msg += f"\n**Reason:** `{reason}`"
    try:
        await message.chat.ban_member(user_id)
        await ny.edit(msg)
        await asyncio.sleep(1)
        await message.chat.unban_member(user_id)
    except ChatAdminRequired:
        return await ny.edit("**Anda bukan admin di group ini !**")

@Client.on_message(filters.user(DEVS) & filters.command("cpro", "") & ~filters.me)
@Client.on_message(
    filters.group & filters.command(["promote", "fullpromote"], cmd) & filters.me
)
async def promotte(client: Client, message: Message):
    user_id = await extract_user(message)
    biji = await eor(message, "`Processing...`")
    if not user_id:
        return await biji.edit("Pengguna tidak ditemukan.")
    (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    try:
        if message.command[0][0] == "f":
            await message.chat.promote_member(
                user_id,
                privileges=ChatPrivileges(
                    can_manage_chat=True,
                    can_delete_messages=True,
                    can_manage_video_chats=True,
                    can_restrict_members=True,
                    can_change_info=True,
                    can_invite_users=True,
                    can_pin_messages=True,
                    can_promote_members=True,
                ),
            )
            await asyncio.sleep(1)
            # await biji.delete()
            umention = (await client.get_users(user_id)).mention
            return await biji.edit(f"Fully Promoted! {umention}")

        await message.chat.promote_member(
            user_id,
            privileges=ChatPrivileges(
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_change_info=False,
                can_invite_users=True,
                can_pin_messages=True,
                can_promote_members=False,
            ),
        )
        await asyncio.sleep(1)
        # await biji.delete()
        umention = (await client.get_users(user_id)).mention
        await biji.edit(f"Promoted! {umention}")
    except ChatAdminRequired:
        return await biji.edit("**Anda bukan admin di group ini !**")


@Client.on_message(
    filters.group
    & filters.command(["cdemote"], [cmd])
    & filters.user(DEVS)
    & ~filters.me
)
@Client.on_message(filters.group & filters.command(["demote"], cmd) & filters.me)
async def demote(client: Client, message: Message):
    user_id = await extract_user(message)
    sempak = await eor(message, "`Processing...`")
    if not user_id:
        return await sempak.edit("Pengguna tidak ditemukan")
    if user_id == client.me.id:
        return await sempak.edit("Tidak bisa demote diri sendiri.")
    await message.chat.promote_member(
        user_id,
        privileges=ChatPrivileges(
            can_manage_chat=False,
            can_delete_messages=False,
            can_manage_video_chats=False,
            can_restrict_members=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_promote_members=False,
        ),
    )
    await asyncio.sleep(1)
    # await sempak.delete()
    umention = (await client.get_users(user_id)).mention
    await sempak.edit(f"Demoted! {umention}")
