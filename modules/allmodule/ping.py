"""##---------------------------------------------------------##
github : https://github.com/hakutakaid
thanks to kenapanan from naya-pyro
thanks to risman for pyroman-userbot

##---------------------------------------------------------##"""
import time
from datetime import datetime
from random import choice
from random import randint
from pyrogram import *
from pyrogram.raw.functions import Ping
from pyrogram.types import *

from modules.config import cmd, DEVS

START_TIME = datetime.now()

async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append(f'{amount}{unit}{"" if amount == 1 else ""}')
    return ":".join(parts)

TIME_DURATION_UNITS = (
    ("w", 60 * 60 * 24 * 7),
    ("d", 60 * 60 * 24),
    ("h", 60 * 60),
    ("m", 60),
    ("s", 1),
)
@Client.on_message(filters.user(DEVS) & filters.command("cping", "") & ~filters.me)
@Client.on_message(filters.command("ping", cmd) & filters.me)
async def _(client, message):
    start = time.time()
    current_time = datetime.now()
    await client.invoke(Ping(ping_id=randint(0, 2147483647)))
    delta_ping = round((time.time() - start) * 1000, 3)
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    _ping = f"""
<b>❏ Pong !!</b> `{delta_ping} ms`
<b>╰ Aktif:</b> `{uptime}`
"""
    await message.reply(_ping)