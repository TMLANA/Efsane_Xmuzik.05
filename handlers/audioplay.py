# Bu modül yalnızca ses dosyası, IDK kullanarak müzik çalmak için oluşturdum, çünkü play.py modülündeki ses çalar çalışmıyor
# bu yüzden alternatif budur 
# ses çalma işlevi 

from os import path

from pyrogram import Client
from pyrogram.types import Message, Voice

from callsmusic import callsmusic, queues

import converter
from downloaders import youtube

from config import BOT_NAME as bn, DURATION_LIMIT, UPDATES_CHANNEL, AUD_IMG, GROUP_SUPPORT, OWNER_NAME
from helpers.filters import command, other_filters
from helpers.decorators import errors
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(command("mp3") & other_filters)
@errors
async def mp3(_, message: Message):

    lel = await message.reply("🔁 **İşleme alındı** müzik...")
    sender_id = message.from_user.id
    sender_name = message.from_user.first_name

    keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="👮‍♂️ Sahip",
                        url=f"https://t.me/Furkanbeyy"),
                    InlineKeyboardButton(
                        text="🕊️ Kanal​",
                        url=f"https://t.me/SohbetDestek")
                 ],
                 [
                    InlineKeyboardButton(
                        text="👨‍💻 Bot Sahibi",
                        url=f"https://t.me/Mahoaga")
                ]
            ]
        )

    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"❎ Daha fazla şarkı çalınamıyor {DURATION_LIMIT}!"
            )

        file_name = get_file_name(audio)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )
    elif url:
        file_path = await converter.convert(youtube.download(url))
    else:
        return await lel.edit_text("❎ bana çalmam için müzik veya YouTube bağlantıları vermiyorsunuz!")

    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        costumer = message.from_user.mention
        flname = file_name
        await message.reply_photo(
        photo=f"{AUD_IMG}",
        reply_markup=keyboard,
        caption=f"💡  Şarkınız **sıra!**\n\n🏷 İsmi : {flname} \n🎧 İstek üzerine {costumer}")
        return await lel.delete()
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        costumer = message.from_user.mention
        flname = file_name
        await message.reply_photo(
        photo=f"{AUD_IMG}",
        reply_markup=keyboard,
        caption=f"▶️ **Oynatılıyor**\n\n🏷 İsmi : {flname} \n🎧 İstek üzerine {costumer}!"
        )
        return await lel.delete()
