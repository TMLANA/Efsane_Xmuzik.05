# Module by https://github.com/tofikdn
# Copyright (C) 2021 TdMusic

import requests
from config import BOT_USERNAME
from pyrogram import Client
from helpers.filters import command


@Client.on_message(command(["söz", f"söz@{BOT_USERNAME}"]))
async def söz(_, message):
    try:
        if len(message.command) < 2:
            await message.reply_text("`Kasih judul lagunya lah blok!!!`")
            return
        query = message.text.split(None, 1)[1]
        rep = await message.reply_text("`Searching lyrics...`")
        resp = requests.get(f"https://api-tede.herokuapp.com/api/lirik?l={query}").json()
        result = f"{resp['data']}"
        await rep.edit(result)
    except Exception:
        await rep.edit("`Şarkı sözleri bulunamadı !`\n\n• `Daha net bir başlık parçası bulmaya çalışın.`")
