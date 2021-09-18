# (C) Efsane Müzikal herkes için en güzel müzik botu.. 

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
                        "👥 Destek Kanalı", url=f"https://t.me/Sohbetdestek")
                ],
                [
                    InlineKeyboardButton(
                        "📚 Botun Komutları", callback_data="cbhelp"
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
                        "📚 Temel Komutlar", callback_data="cbbasic"
                    ),
                    InlineKeyboardButton(
                        "📕 Gelişmiş Komutlar", callback_data="cbadvanced"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📘 Admin Komutları", callback_data="cbadmin"
                    ),
                    InlineKeyboardButton(
                        "📗 Kullanıcı Komutları", callback_data="cbsudo"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "♥️ Şaka komutları", callback_data="cbfun"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Geri", callback_data="cbguide"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbbasic"))
async def cbbasic(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🕊️ Botlar için temel komutlar</b>

💡 [ GRUP AYARLAMA ]
/play (Başlık) - Youtube üzerinden müzik çalma 
/ytp (Başlık) - Doğrudan müzik çalma 
/mp3 (Sesi yanıtlama) - sesli yanıt yoluyla makbuzları çalma 
/playlist - sıra listesine bakın 
/song (Başlık) - Youtube'dan müzik indirme 
/search (Başlık) - Youtube'dan detaylı müzik arayın 
/video (Başlık) - Youtube'dan ayrıntılı olarak müzik indirin
/lirik - (Başlık) şarkı sözleri arıyor 
💡 [ KANAL AYARLAMA ]
/cplay - Kanallar üzerinden müzik çalma
/cplayer - sıra listesine bakın 
/cpause - müzik çalar duraklatma 
/cresume - devam eden müzik çalma 
/cskip - Sonraki şarkıya geçme 
/cend - Müziği durdurma 
/admincache - yönetici önbelleğini yenileme 
/ubjoinc - yardım katılmayı kanala davet etme 

💡 Bot Tarafından @SohbetDestek""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Geri", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbadvanced"))
async def cbadvanced(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🕊️ Gelişmiş komut</b>

/start (grupta) - bot durumunu görüntüleme 
/reload - botları güncelleştirme ve yönetici listelerini yenileme 
/alive - canlı botun durumunu görmek 
/ping - ping bot'larını denetleme
/id - kullanıcı id bilgisi çıkartır

💡 Bot Tarafından @SohbetDestek""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Geri", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbadmin"))
async def cbadmin(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🕊️ Grup yöneticisi komutu</b>

/player - kayıttan yürütme durumunu görüntüleme 
/pause - çalan müziği duraklatma 
/resume - Duraklatmadaki müziğe devam et 
/skip - Sonraki şarkıya geçme 
/end - Müziği kapatma 
/userbotjoin - Yardımcıları gruba katılmaya davet etme 
/musicplayer (on / off) - Devre Dışı Bırak / grubunuzdaki müzik çaları açma
/auth - Üye için botu kullanmasına olanak sağlamak (Yetkilendirme)
deauth - üyenin botu kullanma yetkisini almak için (Yetkisizleştirme) 

💡 Bot Tarafından @SohbetDestek""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Geri", callback_data="cbhelp"
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
/gcast - yardımcılar aracılığıyla genel iletiler gönderme 
/rmd - karşıdan yükleme dosyasını silme 
/rmr - indirilen ham dosyaları silme 

💡 Bot Tarafından @SohbetDestek**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Geri", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbfun"))
async def cbfun(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🕊️ **Komut eğlencesi**</b>

**/chika - Kendinizi kontrol edin 
/wibu - Kendinizi kontrol edin
/asupan - Kendinizi kontrol edin
/truth - Kendinizi kontrol edin
/dare - Kendinizi kontrol edin

💡 Bot Tarafından @SohbetDestek**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Geri", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbguide"))
async def cbguide(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**BU BOT NASIL KULLANILIR? :**

**1.) İlk olarak, grubunuza ekleyin..
2.) Ardından anonim yöneticiler dışındaki tüm izinlere sahip bir yönetici oluşturun.
3.) Grubunuza @Sesmusicasistan ekleyin veya `/userbotjoin` asistanları davet etmek için.
4.) Müzik çalmadan önce sesli sohbeti açma.

💡 Bot Tarafından @SohbetDestek**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📚 Komut Listesi", callback_data="cbhelp"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🚪 Çıkış", callback_data="close"
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
                        "📚 Temel Komutlar", callback_data="cbbasic"
                    ),
                    InlineKeyboardButton(
                        "📕 Gelişmiş Komutlar", callback_data="cbadvanced"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📘 Admin Komutları", callback_data="cbadmin"
                    ),
                    InlineKeyboardButton(
                        "📗 Kullanıcı Komutları", callback_data="cbsudo"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "♥️ Şaka Komutları", callback_data="cbfun"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Geri", callback_data="cbstart"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbhowtouse"))
async def cbguides(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🕊️** BOTLAR NASIL KULLANILIR? 🕊️ :

1.) İlk olarak, grubunuza ekleyin..
2.) Ardından anonim yöneticiler dışındaki tüm izinlere sahip bir yönetici oluşturun.
3.) Grubunuza @Sesmusicasistan ekleyin veya `/userbotjoin` asistanları davet etmek için.
4.) Müzik çalmadan önce sesli sohbeti açma.

💡 Bot Tarafından @SohbetDestek**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Geri", callback_data="cbstart"
                    )
                ]
            ]
        )
    )
