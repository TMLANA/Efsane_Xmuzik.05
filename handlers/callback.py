# (C) supun-maduraga my best friend for his project on call-music-plus

from time import time
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery
from helpers.decorators import authorized_users_only
from config import BOT_NAME, BOT_USERNAME, OWNER_NAME, GROUP_SUPPORT, UPDATES_CHANNEL, ASSISTANT_NAME
from handlers.play import cb_admin_check


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


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await query.edit_message_text(
        f"""<b>👋🏻 **Merhaba, Ben {query.message.from_user.mention}!**</b>

✅ **Aktifim ve müzik çalmaya hazırım.!
• Başlangıç saati: `{START_TIME_ISO}`
• Düğmeye tıklayın » 📚 Tüm bot komutlarını komutla ve görüntüle!

💡 Bot tarafından @SohbetDestek**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "👥 Support", url=f"https://t.me/Sohbetdestek")
                ],
                [
                    InlineKeyboardButton(
                        "📚 Komut", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )



@Client.on_callback_query(filters.regex("cbhelp"))
async def cbhelp(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🕊️ İşte yardım menüsü.!</b>

**Bu menüde, mevcut birkaç komut menüsünü açabilirsiniz, her komut menüsünde her komutun kısa bir açıklaması da vardır**

💡 Bot Tarafından @SohbetDestek""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📚 Temel komutlar", callback_data="cbbasic"
                    ),
                    InlineKeyboardButton(
                        "📕 İleri komutlar", callback_data="cbadvanced"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📘 Admin komutları", callback_data="cbadmin"
                    ),
                    InlineKeyboardButton(
                        "📗 Kullanıcı komutları", callback_data="cbsudo"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "♥️ Şaka komutları", callback_data="cbfun"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "BACK", callback_data="cbguide"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbbasic"))
async def cbbasic(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🕊️ Botlar için temel komutlar</b>

💡 [ SETTING GRUP ]
/play (judul) - memutar musik melalui youtube
/ytp (judul) - memutar musik secara langsung 
/stream (balas ke audio) - memutar kusik melalui balas ke audio
/playlist - melihat daftar antrian
/song (judul) - mengunduh musik dari youtube
/search (judul) - mencari musik dari youtube secara detail
/video (judul) - mengunduh musik dari youtube secara detail
/lirik - (judul) mencari lirik
💡 [ SETTING CHANNEL ]
/cplay - memutar musik melalui channel
/cplayer - melihat daftar antrian
/cpause - jeda pemutar musik
/cresume - melanjut pemutaran musik
/cskip - melewati ke lagu berikutnya
/cend - memberhentikan musik
/admincache - menyegarkan cache admin
/ubjoinc - mengundang assisten join ke channel

💡 Bot Tarafından @SohbetDestek""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "BACK", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbadvanced"))
async def cbadvanced(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🕊️ Gelişmiş komut</b>

/start (di grup) - melihat status bot
/reload - memperbarui bot dan menyegarkan daftar admin
/alive - melihat status alive bot
/ping - cek ping bot

💡 Bot Tarafından @SohbetDestek""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "BACK", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbadmin"))
async def cbadmin(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🕊️ Grup yöneticisi komutu</b>

/player - melihat status pemutaran
/pause - jeda musik yang diputar
/resume - melanjutkan musik yang di jeda
/skip - melewati ke lagu berikutnya
/end - mematikan musik
/userbotjoin - mengundang assistant untuk bergabung ke grup
/musicplayer (on / off) - mematikan / menghidupkan pemutar musik di grupmu

💡 Bot Tarafından @SohbetDestek""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "BACK", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbsudo"))
async def cbsudo(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🕊️ **Kullanıcı komutu**</b>

**/userbotleaveall - mengeluarkan asisten dari semua grup
/gcast - mengirim pesan global melalui asisten
/rmd - menghapus file downloadan
/rmr - menghapus file raw terdownload

💡 Bot Tarafından @SohbetDestek**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "BACK", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbfun"))
async def cbfun(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🕊️ **Komut eğlencesi**</b>

**/chika - cek sendiri
/wibu - cek sendiri
/asupan - cek sendiri
/truth - cek sendiri
/dare - cek sendiri

💡 Bot Tarafından @SohbetDestek**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "BACK", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbguide"))
async def cbguide(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**BU BOT NASIL KULLANILIR? :**

**1.) Pertama, tambahkan ke grupmu.
2.) Kemudian jadikan admin dengan semua izin kecuali admin anonim.
3.) Tambahkan @Sesmusicasistan ke grupmu atau bisa ketik `/userbotjoin` untuk mengundang assistant.
4.) Nyalakan obrolan suara terlebih dahulu sebelum memutar musik.

💡 Bot Tarafından @SohbetDestek**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📚 Command List", callback_data="cbhelp"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🗑 Close", callback_data="close"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("close"))
async def close(_, query: CallbackQuery):
    await query.message.delete()


@Client.on_callback_query(filters.regex("cbcmds"))
async def cbhelps(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🕊️ **Bu yardım menüsü.!**</b>

**Bu menüde, mevcut birkaç komut menüsünü açabilirsiniz, her komut menüsünde her komutun kısa bir açıklaması da vardır

💡 Bot Tarafından @SohbetDestek**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📚 Temel Cmd", callback_data="cbbasic"
                    ),
                    InlineKeyboardButton(
                        "📕 İleri Cmd", callback_data="cbadvanced"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📘 Admin Cmd", callback_data="cbadmin"
                    ),
                    InlineKeyboardButton(
                        "📗 Kullanıcı Cmd", callback_data="cbsudo"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "♥️ Şaka Cmd", callback_data="cbfun"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "BACK", callback_data="cbstart"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbhowtouse"))
async def cbguides(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🕊️** BOTLAR NASIL KULLANILIR? 🕊️ :

1.) Pertama, tambahkan ke grupmu.
2.) Kemudian jadikan admin dengan semua izin kecuali admin anonim.
3.) Tambahkan @Sesmusicasistan ke grupmu atau bisa ketik `/userbotjoin` untuk mengundang assistant.
4.) Nyalakan obrolan suara terlebih dahulu sebelum memutar musik.

💡 Bot Tarafından @SohbetDestek**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "BACK", callback_data="cbstart"
                    )
                ]
            ]
        )
    )
