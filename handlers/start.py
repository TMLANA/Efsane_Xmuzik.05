from time import time
from datetime import datetime
from config import BOT_USERNAME, BOT_NAME, ASSISTANT_NAME, OWNER_NAME, UPDATES_CHANNEL, GROUP_SUPPORT
from helpers.filters import command
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from helpers.decorators import authorized_users_only


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)


@Client.on_message(command("start") & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>🕊️ **Hallo {message.from_user.mention}** \n
**__[EfsaneMusicBot](https://t.me/Mp3dinleme_Bot) Telegram sesli sohbetinde müzik çalmak için tasarlanmış bir bottur!__**
**__Untuk melihat beberapa perintah dalam penggunaan bot bisa klik » /help__**
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
                    InlineKeyboardButton(
                        "➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ​ ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],[
                    InlineKeyboardButton(
                        "sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/Sohbetdestek"
                    ),
                    InlineKeyboardButton(
                        "ᴜᴘᴅᴀᴛᴇs", url=f"https://t.me/kurtadamoyunuu")
                ],[
                    InlineKeyboardButton(
                        "sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ​", url="https://github.com/Mehmetbaba55/EfsaneXMusic"
                    )
                ]
            ]
        )
    )


@Client.on_message(command(["start", f"start@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def start(client: Client, message: Message):
    start = time()
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    delta_ping = time() - start
    await message.reply_text(
        f"""<b>👋🏻 **Merhaba {message.from_user.mention()}!**</b>

✅ **Aktifim ve müzik çalmaya hazırım.!
• Hız : {delta_ping * 1000:.3f} ms
• Başlangıç saati: `{START_TIME_ISO}`
• Düğmeye tıklayın » 📚 **Komut** ve tüm bot komutlarına bakın!
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "👥 Support", url=f"https://t.me/Sohbetdestek")
                ],
                [
                    InlineKeyboardButton(
                        "📚 Komut", callback_data="cbcmds"
                    )
                ]
            ]
        )
    )


@Client.on_message(command(["help", f"help@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def help(client: Client, message: Message):
    await message.reply_text(
        f"""<b>👋🏻 **Merhaba** {message.from_user.mention()}</b>
**Açıklamayı okumak ve kullanılabilir komutların listesini görmek için lütfen aşağıdaki düğmeye basın!**

💡 Bot Tarafından @SohbetDestek""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=" BENI NASIL KULLANARSIN?", callback_data=f"cbguide"
                    )
                ]
            ]
        )
    )

@Client.on_message(command("help") & filters.private & ~filters.edited)
async def help_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>💡 **Merhaba {message.from_user.mention} yardım menüsüne hoş geldiniz!**</b>

**__Bu menüde birkaç kullanılabilir komut menüsü açabilirsiniz, her komut menüsünde her komutun kısa bir açıklaması da vardır__**

💡 Bot Tarafından @SohbetDestek""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "HELP", callback_data="cbhowtouse"
                    )
                ]
            ]
        )
    )


@Client.on_message(filters.command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    delta_ping = time() - start
    await message.reply_text(
        f"**Pong!!** {delta_ping * 1000:.3f} ms\n"
        f"• **Uptime:** `{uptime}`\n"
        f"• **başlangıç saati:** `{START_TIME_ISO}`"
    )
