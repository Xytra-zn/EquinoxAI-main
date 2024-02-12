import platform
import config
import psutil
import time
from pyrogram.types import InputMediaVideo
import random
from Equinox import Equinox
from pyrogram import Client, filters
from pyrogram.types import Message

start_time = time.time()


PING_SRC = "https://images.mingming.dev/file/0332bf14f59e465faf1e6.jpg"



def time_formatter(milliseconds):
    minutes, seconds = divmod(int(milliseconds / 1000), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    tmp = (((str(weeks) + "ᴡ:") if weeks else "") +
           ((str(days) + "ᴅ:") if days else "") +
           ((str(hours) + "ʜ:") if hours else "") +
           ((str(minutes) + "ᴍ:") if minutes else "") +
           ((str(seconds) + "s") if seconds else ""))
    if not tmp:
        return "0s"
    if tmp.endswith(":"):
        return tmp[:-1]
    return tmp

@Equinox.on_message(filters.command("ping"))
async def activevc(_, message: Message):
    uptime = time_formatter((time.time() - start_time) * 1000)
    cpu = psutil.cpu_percent()
    storage = psutil.disk_usage('/')
    
    python_version = platform.python_version()

    TEXT = (
       "**๏─╼⃝𖠁๏𝖯𝖨𝖭𝖦🏓 𝖯𝖮𝖭𝖦๏𖠁⃝╾─๏**\n\n"
        f" ⦿ 𝖴𝖯𝖣𝖠𝖳𝖤 🔄 ➠ {uptime}\n"
        f" ⦿ 𝖢𝖯𝖴 ⚙️ ➠ {cpu}%\n"
        f" ⦿ 𝖲𝖳𝖮𝖱𝖠𝖦𝖤 💾 ➠ {size_formatter(storage.total)}\n"
        f" ⦿ 𝖴𝖲𝖤𝖣 📊 ➠ {size_formatter(storage.used)}\n"
        f" ⦿ 𝖥𝖱𝖤𝖤 🗃️ ➠ {size_formatter(storage.free)}\n"
        f" ⦿ 𝖯𝖸𝖳𝖧𝖮𝖭 𝖵𝖤𝖱𝖲𝖨𝖮𝖭 🐍➠ {python_version}\n"
    )

    await message.reply_photo(
    photo=PING_SRC,
    caption=TEXT,
     )


def size_formatter(bytes, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(bytes) < 1024.0:
            return "%3.1f %s%s" % (bytes, unit, suffix)
        bytes /= 1024.0
    return "%.1f %s%s" % (bytes, 'Y', suffix)
