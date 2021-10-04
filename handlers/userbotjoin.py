from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
import asyncio
from helpers.decorators import authorized_users_only, errors
from callsmusic.callsmusic import client as USER
from config import SUDO_USERS


@Client.on_message(filters.command(["انضم"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>**Önce beni yönetici yap.!**</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "helper"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "__**Saya bergabung ke grup untuk memutar musik**__")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>Userbot zaten sohbette</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 Flood Wait Error 🛑 \n {user.first_name} kullanıcısı, userbot için yoğun katılma istekleri nedeniyle grubunuza katılamadı! Kullanıcının grupta yasaklı olmadığından emin olun."
            "\n\nVeya Grubunuza el ile Asisstant ekleyin ve yeniden deneyin</b>",
        )
        return
    await message.reply_text(
        "<b>🕊️ **Asistan gruba katılır**</b>",
    )


@Client.on_message(filters.group & filters.command(["غادر"]))
@authorized_users_only
async def rem(client, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            f"<b>Kullanıcı grubunuzdan ayrılamadı! Floodwaits olabilir."
            "\n\nYa da beni manuel olarak grubunuza tekmelersiniz.</b>",
        )
        return

    
@Client.on_message(filters.command(["userbotleaveall"]))
async def bye(client, message):
    if message.from_user.id in SUDO_USERS:
        left=0
        failed=0
        lol = await message.reply("Asistan Tüm sohbetleri bırakma")
        async for dialog in USER.iter_dialogs():
            try:
                await USER.leave_chat(dialog.chat.id)
                left = left+1
                await lol.edit(f"Asistan ayrılıyor... Left: {left} chats. Failed: {failed} chats.")
            except:
                failed=failed+1
                await lol.edit(f"Asistan ayrılıyor... Left: {left} chats. Failed: {failed} chats.")
            await asyncio.sleep(0.7)
        await client.send_message(message.chat.id, f"Left {left} chats. Failed {failed} chats.")


@Client.on_message(filters.command(["userbotjoinchannel","ubjoinc"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addcchannel(client, message):
    try:
      conchat = await client.get_chat(message.chat.id)
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("sohbet bile bağlantılı mı ?")
      return    
    chat_id = chid
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>önce beni grup yöneticisi olarak terfi ettir !</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "helper"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "🤖: istediğiniz gibi buraya katıldım")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>kanalınızda zaten yardımcı</b>",
        )
        return
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 Flood Wait Error 🛑 \n User {user.first_name} couldn't join your channel due to heavy join requests for userbot! Make sure user is not banned in channel."
            f"\n\nVeya el ile ekleme @{ASSISTANT_NAME} grubunuza ve yeniden deneyin</b>",
        )
        return
    await message.reply_text(
        "<b>yardımcı userbot kanalınıza katıldı</b>",
    )
