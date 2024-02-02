# Copyright (C) @subinps
# Update By (C) @theSmartBisnu
# Channel : https://t.me/itsSmartDev

from utils import LOGGER
import json
import os
from pyrogram.types import Message
from contextlib import suppress
from config import Config
from utils import (
    get_buttons, 
    is_admin, 
    get_playlist_str, 
    shuffle_playlist, 
    import_play_list, 
    delete_messages,
    chat_filter
)
from pyrogram import (
    Client, 
    filters
)
from pyrogram.errors import (
    MessageNotModified, 
    MessageIdInvalid
)


admin_filter=filters.create(is_admin)   


@Client.on_message(filters.command(["export", f"export@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def export_play_list(client, message: Message):
    if not Config.playlist:
        k=await message.reply_text("Playlist is Empty")
        await delete_messages([message, k])
        return
    file=f"{message.chat.id}_{message.message_id}.json"
    with open(file, 'w+') as outfile:
        json.dump(Config.playlist, outfile, indent=4)
    await client.send_document(chat_id=message.chat.id, document=file, file_name="PlayList.json", caption=f"Playlist\n\nNumber Of Songs: <code>{len(Config.playlist)}</code>\n\nJoin [XTZ Bots](https://t.me/subin_works)")
    try:
        os.remove(file)
    except:
        pass
    await delete_messages([message])

@Client.on_message(filters.command(["import", f"import@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def import_playlist(client, m: Message):
    with suppress(MessageIdInvalid, MessageNotModified):
        if m.reply_to_message is not None and m.reply_to_message.document:
            if m.reply_to_message.document.file_name != "PlayList.json":
                k=await m.reply("Invalid PlayList file given. Export your current Playlist using /export.")
                await delete_messages([m, k])
                return
            myplaylist=await m.reply_to_message.download()
            status=await m.reply("Trying to get details from playlist.")
            n=await import_play_list(myplaylist)
            if not n:
                await status.edit("Errors Occured while importing playlist.")
                await delete_messages([m, status])
                return
            if Config.SHUFFLE:
                await shuffle_playlist()
            pl=await get_playlist_str()
            if m.chat.type == "private":
                await status.edit(pl, disable_web_page_preview=True, reply_markup=await get_buttons())        
            elif not Config.LOG_GROUP and m.chat.type == "supergroup":
                if Config.msg.get('playlist'):
                    await Config.msg['playlist'].delete()
                Config.msg['playlist'] = await status.edit(pl, disable_web_page_preview=True, reply_markup=await get_buttons())
                await delete_messages([m])
            else:
                await delete_messages([m, status])
        else:
            k = await m.reply("No playList file given.")
            await delete_messages([m, k])
