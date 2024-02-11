# Copyright (C) @subinps
# Update By (C) @theSmartBisnu
# Channel : https://t.me/itsSmartDev


from utils import LOGGER
from pyrogram.types import Message
from pyrogram import enums
from config import Config
from pyrogram.errors import ChannelInvalid
from pyrogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton
    )
import base64
from pyrogram import (
    Client, 
    filters
)
from utils import (
    clear_db_playlist, 
    get_playlist_str, 
    is_admin, 
    mute, 
    restart_playout, 
    settings_panel, 
    skip, 
    pause, 
    resume, 
    unmute, 
    volume, 
    get_buttons, 
    is_admin, 
    seek_file, 
    delete_messages,
    chat_filter,
    volume_buttons
)

admin_filter=filters.create(is_admin)   

@Client.on_message(filters.command(["playlist", f"playlist@{Config.BOT_USERNAME}"]))
async def player(client, message):
    # Check if the command is used in a group chat
    if message.chat.type != enums.ChatType.PRIVATE:
        # Check if the command is used in the authorized chat
        if message.chat.id != Config.CHAT:
            buttons = [
                [
                    InlineKeyboardButton(base64.b32decode('====A25NCCI4W35JAJZWWQVJARFJ2PC6'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('======IOFL6CGWBKDSVIHZFMN3U6S4FMSL54WZFNC3L2WXNMORYKHUROJ3Z6SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8')),
                    InlineKeyboardButton(base64.b32decode('===KGZVMICI4WU5NKCIKIOK4'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8')),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await message.reply(
                "This is not the group which I have been configured to play in. Do you want to set this group as default CHAT?",
                quote=False,
                reply_markup=reply_markup
            )
            return

        administrators = []
        async for member in client.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            administrators.append(member.user.id)

        # Check if the user is an admin or in the Config.ADMINS list
        if message.from_user.id not in administrators and message.from_user.id not in Config.ADMINS:
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(base64.b32decode('====QCSTCHIOXXZJAR3SWXJJ'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8'))]
            ])
            await client.send_message(
                chat_id=message.chat.id,
                text=base64.b32decode('6RY6C6QR5UYBCSVM2L2EXXBNUL5CGQQOPT3ASSJOBDIKXXFPABLSHZJOP3U4DRRH'[::-1].encode('utf-8')).decode('utf-8'),
                reply_markup=reply_markup
            )
            return
    else:
        # Handle unauthorized users in a private chat
        if message.from_user.id not in Config.ADMINS:
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(base64.b32decode('====QCSTCHIOXXZJAR3SWXJJ'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8'))]
            ])
            await client.send_message(
                chat_id=message.chat.id,
                text=base64.b32decode('6RY6C6QR5UYBCSVM2L2EXXBNUL5CGQQOPT3ASSJOBDIKXXFPABLSHZJOP3U4DRRH'[::-1].encode('utf-8')).decode('utf-8'),
                reply_markup=reply_markup
            )
            return

    # Rest of the code remains the same
    if not Config.CALL_STATUS:
        await message.reply_text(
            "<b>Player is idle, start the player using the below button.</b>",
            quote=False,
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
        await delete_messages([message])
        return

    pl = await get_playlist_str()
    if message.chat.type == enums.ChatType.PRIVATE:
        await message.reply_text(
            pl,
            disable_web_page_preview=True,
            reply_markup=await get_buttons(),
        )
    else:
        if Config.msg.get('player') is not None:
            await Config.msg['player'].delete()
        Config.msg['player'] = await message.reply_text(
            pl,
            disable_web_page_preview=True,
            quote=False,
            reply_markup=await get_buttons(),
        )
    await delete_messages([message])



@Client.on_message(filters.command(["skip", f"skip@{Config.BOT_USERNAME}"]))
async def skip_track(client, message):
    # Check if the command is used in a group chat
    if message.chat.type != enums.ChatType.PRIVATE:
        # Check if the command is used in the authorized chat
        if message.chat.id != Config.CHAT:
            buttons = [
                [
                    InlineKeyboardButton(base64.b32decode('====A25NCCI4W35JAJZWWQVJARFJ2PC6'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('======IOFL6CGWBKDSVIHZFMN3U6S4FMSL54WZFNC3L2WXNMORYKHUROJ3Z6SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8')),
                    InlineKeyboardButton(base64.b32decode('===KGZVMICI4WU5NKCIKIOK4'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8')),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await message.reply(
                "This is not the group which I have been configured to play in. Do you want to set this group as default CHAT?",
                quote=False,
                reply_markup=reply_markup
            )
            return

        administrators = []
        async for member in client.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            administrators.append(member.user.id)

        # Check if the user is an admin or in the Config.ADMINS list
        if message.from_user.id not in administrators and message.from_user.id not in Config.ADMINS:
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(base64.b32decode('====QCSTCHIOXXZJAR3SWXJJ'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8'))]
            ])
            await client.send_message(
                chat_id=message.chat.id,
                text=base64.b32decode('6RY6C6QR5UYBCSVM2L2EXXBNUL5CGQQOPT3ASSJOBDIKXXFPABLSHZJOP3U4DRRH'[::-1].encode('utf-8')).decode('utf-8'),
                reply_markup=reply_markup
            )
            return
    else:
        # Handle unauthorized users in a private chat
        if message.from_user.id not in Config.ADMINS:
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(base64.b32decode('====QCSTCHIOXXZJAR3SWXJJ'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8'))]
            ])
            await client.send_message(
                chat_id=message.chat.id,
                text=base64.b32decode('6RY6C6QR5UYBCSVM2L2EXXBNUL5CGQQOPT3ASSJOBDIKXXFPABLSHZJOP3U4DRRH'[::-1].encode('utf-8')).decode('utf-8'),
                reply_markup=reply_markup
            )
            return

    # Rest of the code remains the same
    msg = await client.send_message(chat_id=message.chat.id, text='<b>Trying to skip from queue...</b>')
    should_delete_msg = True
    try:
        if not Config.CALL_STATUS:
            await msg.edit("Player is idle, start the player using the button below.", disable_web_page_preview=True, quote=False, reply_markup=await get_buttons())
            return
        if not Config.playlist:
            await msg.edit("<b>Bruh! Playlist is empty.</b>")
            should_delete_msg = False  # Don't delete this message
            return
        if len(message.command) == 1:
            await skip()
        else:
            try:
                items = list(dict.fromkeys(message.command[1:]))
                items = [int(x) for x in items if x.isdigit()]
                items.sort(reverse=True)
                for i in items:
                    if 2 <= i <= (len(Config.playlist) - 1):
                        await msg.edit(f"Succesfully Removed from Playlist- {i}. **{Config.playlist[i][1]}**")
                        await clear_db_playlist(song=Config.playlist[i])
                        Config.playlist.pop(i)
                    else:
                        await msg.edit(f"You can't skip first two songs- {i}")
            except (ValueError, TypeError):
                await msg.edit("Invalid input")
        pl = await get_playlist_str()
        if message.chat.type == "private":
            await msg.edit(pl, disable_web_page_preview=True, reply_markup=await get_buttons())
        elif not Config.LOG_GROUP and message.chat.type == "supergroup":
            if Config.msg.get('player'):
                await Config.msg['player'].delete()
            Config.msg['player'] = await msg.edit(pl, disable_web_page_preview=True, reply_markup=await get_buttons())
    finally:
        if should_delete_msg:
            await msg.delete()
            print("Message deleted.")
        else:
            print("Message not deleted.")
        await delete_messages([message])





@Client.on_message(filters.command(["pause", f"pause@{Config.BOT_USERNAME}"]))
async def pause_playing(client, message):
    # Check if the command is used in a group chat
    if message.chat.type != enums.ChatType.PRIVATE:
        # Check if the command is used in the authorized chat
        if message.chat.id != Config.CHAT:
            buttons = [
                [
                    InlineKeyboardButton(base64.b32decode('====A25NCCI4W35JAJZWWQVJARFJ2PC6'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('======IOFL6CGWBKDSVIHZFMN3U6S4FMSL54WZFNC3L2WXNMORYKHUROJ3Z6SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8')),
                    InlineKeyboardButton(base64.b32decode('===KGZVMICI4WU5NKCIKIOK4'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8')),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await message.reply(
                "This is not the group which I have been configured to play in. Do you want to set this group as default CHAT?",
                quote=False,
                reply_markup=reply_markup
            )
            return

        administrators = []
        async for member in client.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            administrators.append(member.user.id)

        # Check if the user is an admin or in the Config.ADMINS list
        if message.from_user.id not in administrators and message.from_user.id not in Config.ADMINS:
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(base64.b32decode('====QCSTCHIOXXZJAR3SWXJJ'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8'))]
            ])
            await client.send_message(
                chat_id=message.chat.id,
                text=base64.b32decode('6RY6C6QR5UYBCSVM2L2EXXBNUL5CGQQOPT3ASSJOBDIKXXFPABLSHZJOP3U4DRRH'[::-1].encode('utf-8')).decode('utf-8'),
                reply_markup=reply_markup
            )
            return
    else:
        # Handle unauthorized users in a private chat
        if message.from_user.id not in Config.ADMINS:
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(base64.b32decode('====QCSTCHIOXXZJAR3SWXJJ'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8'))]
            ])
            await client.send_message(
                chat_id=message.chat.id,
                text=base64.b32decode('6RY6C6QR5UYBCSVM2L2EXXBNUL5CGQQOPT3ASSJOBDIKXXFPABLSHZJOP3U4DRRH'[::-1].encode('utf-8')).decode('utf-8'),
                reply_markup=reply_markup
            )
            return

    # Rest of the code remains the same
    if not Config.CALL_STATUS:
        await message.reply_text(
            "<b>Player is idle, start the player using the button below.</b>",
            quote=False,
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
        return
    if Config.PAUSE:
        await message.reply("<b>Bruh! Already Paused</b>", quote=False)
        return
    await message.reply("<b>Paused Video Call</b>", quote=False)
    await pause()




    

@Client.on_message(filters.command(["resume", f"resume@{Config.BOT_USERNAME}"]))
async def resume_playing(client, message):
    # Check if the command is used in a group chat
    if message.chat.type != enums.ChatType.PRIVATE:
        # Check if the command is used in the authorized chat
        if message.chat.id != Config.CHAT:
            buttons = [
                [
                    InlineKeyboardButton(base64.b32decode('====A25NCCI4W35JAJZWWQVJARFJ2PC6'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('======IOFL6CGWBKDSVIHZFMN3U6S4FMSL54WZFNC3L2WXNMORYKHUROJ3Z6SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8')),
                    InlineKeyboardButton(base64.b32decode('===KGZVMICI4WU5NKCIKIOK4'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8')),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await message.reply(
                "This is not the group which I have been configured to play in. Do you want to set this group as default CHAT?",
                quote=False,
                reply_markup=reply_markup
            )
            return

        administrators = []
        async for member in client.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            administrators.append(member.user.id)

        # Check if the user is an admin or in the Config.ADMINS list
        if message.from_user.id not in administrators and message.from_user.id not in Config.ADMINS:
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(base64.b32decode('====QCSTCHIOXXZJAR3SWXJJ'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8'))]
            ])
            await client.send_message(
                chat_id=message.chat.id,
                text=base64.b32decode('6RY6C6QR5UYBCSVM2L2EXXBNUL5CGQQOPT3ASSJOBDIKXXFPABLSHZJOP3U4DRRH'[::-1].encode('utf-8')).decode('utf-8'),
                reply_markup=reply_markup
            )
            return
    else:
        # Handle unauthorized users in a private chat
        if message.from_user.id not in Config.ADMINS:
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(base64.b32decode('====QCSTCHIOXXZJAR3SWXJJ'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8'))]
            ])
            await client.send_message(
                chat_id=message.chat.id,
                text=base64.b32decode('6RY6C6QR5UYBCSVM2L2EXXBNUL5CGQQOPT3ASSJOBDIKXXFPABLSHZJOP3U4DRRH'[::-1].encode('utf-8')).decode('utf-8'),
                reply_markup=reply_markup
            )
            return

    # Rest of the code remains the same
    if not Config.CALL_STATUS:
        await message.reply_text(
            "<b>Player is idle, start the player using the button below.</b>",
            quote=False,
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
        return
    if not Config.PAUSE:
        await message.reply("<b>Nothing paused to resume</b>", quote=False)
        return
    await message.reply("<b>Resumed Video Call</b>", quote=False)
    await resume()


    


@Client.on_message(filters.command(['volume', f"volume@{Config.BOT_USERNAME}"]))
async def set_vol(client, message):
    # Check if the command is used in a group chat
    if message.chat.type != enums.ChatType.PRIVATE:
        # Check if the command is used in the authorized chat
        if message.chat.id != Config.CHAT:
            buttons = [
                [
                    InlineKeyboardButton(base64.b32decode('====A25NCCI4W35JAJZWWQVJARFJ2PC6'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('======IOFL6CGWBKDSVIHZFMN3U6S4FMSL54WZFNC3L2WXNMORYKHUROJ3Z6SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8')),
                    InlineKeyboardButton(base64.b32decode('===KGZVMICI4WU5NKCIKIOK4'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8')),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await message.reply(
                "This is not the group which I have been configured to play in. Do you want to set this group as default CHAT?",
                quote=False,
                reply_markup=reply_markup
            )
            return

        administrators = []
        async for member in client.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            administrators.append(member.user.id)

        # Check if the user is an admin or in the Config.ADMINS list
        if message.from_user.id not in administrators and message.from_user.id not in Config.ADMINS:
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(base64.b32decode('====QCSTCHIOXXZJAR3SWXJJ'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8'))]
            ])
            await client.send_message(
                chat_id=message.chat.id,
                text=base64.b32decode('6RY6C6QR5UYBCSVM2L2EXXBNUL5CGQQOPT3ASSJOBDIKXXFPABLSHZJOP3U4DRRH'[::-1].encode('utf-8')).decode('utf-8'),
                reply_markup=reply_markup
            )
            return
    else:
        # Handle unauthorized users in a private chat
        if message.from_user.id not in Config.ADMINS:
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(base64.b32decode('====QCSTCHIOXXZJAR3SWXJJ'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8'))]
            ])
            await client.send_message(
                chat_id=message.chat.id,
                text=base64.b32decode('6RY6C6QR5UYBCSVM2L2EXXBNUL5CGQQOPT3ASSJOBDIKXXFPABLSHZJOP3U4DRRH'[::-1].encode('utf-8')).decode('utf-8'),
                reply_markup=reply_markup
            )
            return

    if not Config.CALL_STATUS:
        await message.reply_text(
            "<b>Player is idle, start the player using the button below.</b>",
            quote=False,
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
        return
    if len(message.command) < 2:
        await message.reply_text('<b>Change Volume of Your VCPlayer.</b>', quote=False, reply_markup=await volume_buttons())
        return
    if not 1 < int(message.command[1]) < 200:
        await message.reply_text("<b>Only 1-200 range is accepted.</b>", quote=False, reply_markup=await volume_buttons())
    else:
        await volume(int(message.command[1]))
        await message.reply_text(f"<b>Succesfully set volume to {message.command[1]}</b>", quote=False, reply_markup=await volume_buttons())

    


@Client.on_message(filters.command(['vcmute', f"vcmute@{Config.BOT_USERNAME}"]))
async def set_mute(client, message):
    # Check if the command is used in a group chat
    if message.chat.type != enums.ChatType.PRIVATE:
        # Check if the command is used in the authorized chat
        if message.chat.id != Config.CHAT:
            buttons = [
                [
                    InlineKeyboardButton(base64.b32decode('====A25NCCI4W35JAJZWWQVJARFJ2PC6'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('======IOFL6CGWBKDSVIHZFMN3U6S4FMSL54WZFNC3L2WXNMORYKHUROJ3Z6SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8')),
                    InlineKeyboardButton(base64.b32decode('===KGZVMICI4WU5NKCIKIOK4'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8')),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await message.reply(
                "This is not the group which I have been configured to play in. Do you want to set this group as default CHAT?",
                quote=False,
                reply_markup=reply_markup
            )
            return

        administrators = []
        async for member in client.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            administrators.append(member.user.id)

        # Check if the user is an admin or in the Config.ADMINS list
        if message.from_user.id not in administrators and message.from_user.id not in Config.ADMINS:
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(base64.b32decode('====QCSTCHIOXXZJAR3SWXJJ'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8'))]
            ])
            await client.send_message(
                chat_id=message.chat.id,
                text=base64.b32decode('6RY6C6QR5UYBCSVM2L2EXXBNUL5CGQQOPT3ASSJOBDIKXXFPABLSHZJOP3U4DRRH'[::-1].encode('utf-8')).decode('utf-8'),
                reply_markup=reply_markup
            )
            return
    else:
        # Handle unauthorized users in a private chat
        if message.from_user.id not in Config.ADMINS:
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(base64.b32decode('====QCSTCHIOXXZJAR3SWXJJ'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8'))]
            ])
            await client.send_message(
                chat_id=message.chat.id,
                text=base64.b32decode('6RY6C6QR5UYBCSVM2L2EXXBNUL5CGQQOPT3ASSJOBDIKXXFPABLSHZJOP3U4DRRH'[::-1].encode('utf-8')).decode('utf-8'),
                reply_markup=reply_markup
            )
            return

    if not Config.CALL_STATUS:
        await message.reply_text(
            "<b>Player is idle, start the player using the button below.</b>",
            disable_web_page_preview=True,
            quote=False,
            reply_markup=await get_buttons()
        )
        return
    if Config.MUTED:
        await message.reply_text("<b>Already muted 🔕</b>", quote=False)
        return
    k = await mute()
    Config.MUTED = True
    if k:
        await message.reply_text(f"<b>Successfully Muted 🔕</b>", quote=False)
    else:
        await message.reply_text("</b>Already muted 🔕</b>", quote=False)

    
@Client.on_message(filters.command(['vcunmute', f"vcunmute@{Config.BOT_USERNAME}"]))
async def set_unmute(client, message):
    # Check if the command is used in a group chat
    if message.chat.type != enums.ChatType.PRIVATE:
        # Check if the command is used in the authorized chat
        if message.chat.id != Config.CHAT:
            buttons = [
                [
                    InlineKeyboardButton(base64.b32decode('====A25NCCI4W35JAJZWWQVJARFJ2PC6'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('======IOFL6CGWBKDSVIHZFMN3U6S4FMSL54WZFNC3L2WXNMORYKHUROJ3Z6SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8')),
                    InlineKeyboardButton(base64.b32decode('===KGZVMICI4WU5NKCIKIOK4'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8')),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await message.reply(
                "This is not the group which I have been configured to play in. Do you want to set this group as default CHAT?",
                quote=False,
                reply_markup=reply_markup
            )
            return

        administrators = []
        async for member in client.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            administrators.append(member.user.id)

        # Check if the user is an admin or in the Config.ADMINS list
        if message.from_user.id not in administrators and message.from_user.id not in Config.ADMINS:
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(base64.b32decode('====QCSTCHIOXXZJAR3SWXJJ'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8'))]
            ])
            await client.send_message(
                chat_id=message.chat.id,
                text=base64.b32decode('6RY6C6QR5UYBCSVM2L2EXXBNUL5CGQQOPT3ASSJOBDIKXXFPABLSHZJOP3U4DRRH'[::-1].encode('utf-8')).decode('utf-8'),
                reply_markup=reply_markup
            )
            return
    else:
        # Handle unauthorized users in a private chat
        if message.from_user.id not in Config.ADMINS:
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(base64.b32decode('====QCSTCHIOXXZJAR3SWXJJ'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8'))]
            ])
            await client.send_message(
                chat_id=message.chat.id,
                text=base64.b32decode('6RY6C6QR5UYBCSVM2L2EXXBNUL5CGQQOPT3ASSJOBDIKXXFPABLSHZJOP3U4DRRH'[::-1].encode('utf-8')).decode('utf-8'),
                reply_markup=reply_markup
            )
            return

    if not Config.CALL_STATUS:
        await message.reply_text(
            "<b>Player is idle, start the player using the button below.</b>",
            quote=False,
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
        return
    if not Config.MUTED:
        await message.reply("<b>Stream already unmuted 🎸</b>", quote=False)
        return
    k = await unmute()
    Config.MUTED = False
    if k:
        await message.reply_text(f"<b>Successfully Unmuted 🎸</b>", quote=False)
    else:
        await message.reply_text("<b>Not muted, already unmuted. 🎸</b>", quote=False)



@Client.on_message(filters.command(["replay", f"replay@{Config.BOT_USERNAME}"]))
async def replay_playout(client, message):
    # Check if the command is used in a group chat
    if message.chat.type != enums.ChatType.PRIVATE:
        # Check if the command is used in the authorized chat
        if message.chat.id != Config.CHAT:
            buttons = [
                [
                    InlineKeyboardButton(base64.b32decode('====A25NCCI4W35JAJZWWQVJARFJ2PC6'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('======IOFL6CGWBKDSVIHZFMN3U6S4FMSL54WZFNC3L2WXNMORYKHUROJ3Z6SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8')),
                    InlineKeyboardButton(base64.b32decode('===KGZVMICI4WU5NKCIKIOK4'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8')),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await message.reply(
                "This is not the group which I have been configured to play in. Do you want to set this group as default CHAT?",
                quote=False,
                reply_markup=reply_markup
            )
            return

        administrators = []
        async for member in client.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            administrators.append(member.user.id)

        # Check if the user is an admin or in the Config.ADMINS list
        if message.from_user.id not in administrators and message.from_user.id not in Config.ADMINS:
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(base64.b32decode('====QCSTCHIOXXZJAR3SWXJJ'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8'))]
            ])
            await client.send_message(
                chat_id=message.chat.id,
                text=base64.b32decode('6RY6C6QR5UYBCSVM2L2EXXBNUL5CGQQOPT3ASSJOBDIKXXFPABLSHZJOP3U4DRRH'[::-1].encode('utf-8')).decode('utf-8'),
                reply_markup=reply_markup
            )
            return
    else:
        # Handle unauthorized users in a private chat
        if message.from_user.id not in Config.ADMINS:
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(base64.b32decode('====QCSTCHIOXXZJAR3SWXJJ'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8'))]
            ])
            await client.send_message(
                chat_id=message.chat.id,
                text=base64.b32decode('6RY6C6QR5UYBCSVM2L2EXXBNUL5CGQQOPT3ASSJOBDIKXXFPABLSHZJOP3U4DRRH'[::-1].encode('utf-8')).decode('utf-8'),
                reply_markup=reply_markup
            )
            return

    msg = await message.reply('<b>Checking player</b>', quote=False)
    if not Config.CALL_STATUS:
        await msg.edit(
            "<b>Player is idle, start the player using the button below.</b>",
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
        return
    await msg.edit(f"<b>Replaying from beginning</b>")
    await restart_playout()



@Client.on_message(filters.command(["player", f"player@{Config.BOT_USERNAME}"]))
async def show_player(client, message):
    # Check if the command is used in a group chat
    if message.chat.type != enums.ChatType.PRIVATE:
        # Check if the command is used in the authorized chat
        if message.chat.id != Config.CHAT:
            buttons = [
                [
                    InlineKeyboardButton(base64.b32decode('====A25NCCI4W35JAJZWWQVJARFJ2PC6'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('======IOFL6CGWBKDSVIHZFMN3U6S4FMSL54WZFNC3L2WXNMORYKHUROJ3Z6SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8')),
                    InlineKeyboardButton(base64.b32decode('===KGZVMICI4WU5NKCIKIOK4'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8')),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await message.reply(
                "This is not the group which I have been configured to play in. Do you want to set this group as default CHAT?",
                quote=False,
                reply_markup=reply_markup
            )
            return

        administrators = []
        async for member in client.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            administrators.append(member.user.id)

        # Check if the user is an admin or in the Config.ADMINS list
        if message.from_user.id not in administrators and message.from_user.id not in Config.ADMINS:
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(base64.b32decode('====QCSTCHIOXXZJAR3SWXJJ'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8'))]
            ])
            await client.send_message(
                chat_id=message.chat.id,
                text=base64.b32decode('6RY6C6QR5UYBCSVM2L2EXXBNUL5CGQQOPT3ASSJOBDIKXXFPABLSHZJOP3U4DRRH'[::-1].encode('utf-8')).decode('utf-8'),
                reply_markup=reply_markup
            )
            return
    else:
        # Handle unauthorized users in a private chat
        if message.from_user.id not in Config.ADMINS:
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(base64.b32decode('====QCSTCHIOXXZJAR3SWXJJ'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8'))]
            ])
            await client.send_message(
                chat_id=message.chat.id,
                text=base64.b32decode('6RY6C6QR5UYBCSVM2L2EXXBNUL5CGQQOPT3ASSJOBDIKXXFPABLSHZJOP3U4DRRH'[::-1].encode('utf-8')).decode('utf-8'),
                reply_markup=reply_markup
            )
            return

    data = Config.DATA.get('FILE_DATA')
    if not data.get('dur', 0) or data.get('dur') == 0:
        title = "<b>Playing Live Stream 🎸</b> ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ"
    else:
        if Config.playlist:
            title = f"<b>{Config.playlist[0][1]}</b>\n ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ"
        elif Config.STREAM_LINK:
            title = f"<b>Stream Using [Url]({data['file']}) </b> ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ"
        else:
            title = f"<b>Streaming Startup [stream]({Config.STREAM_URL})</b> ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ"

    await message.reply_text(
        title,
        quote=False,
        disable_web_page_preview=True,
        reply_markup=await get_buttons()
    )



@Client.on_message(filters.command(["seek", f"seek@{Config.BOT_USERNAME}"]))
async def seek_playout(client, message):
    # Check if the command is used in a group chat
    if message.chat.type != enums.ChatType.PRIVATE:
        # Check if the command is used in the authorized chat
        if message.chat.id != Config.CHAT:
            buttons = [
                [
                    InlineKeyboardButton(base64.b32decode('====A25NCCI4W35JAJZWWQVJARFJ2PC6'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('======IOFL6CGWBKDSVIHZFMN3U6S4FMSL54WZFNC3L2WXNMORYKHUROJ3Z6SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8')),
                    InlineKeyboardButton(base64.b32decode('===KGZVMICI4WU5NKCIKIOK4'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8')),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await message.reply(
                "This is not the group which I have been configured to play in. Do you want to set this group as default CHAT?",
                quote=False,
                reply_markup=reply_markup
            )
            return

        administrators = []
        async for member in client.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            administrators.append(member.user.id)

        # Check if the user is an admin or in the Config.ADMINS list
        if message.from_user.id not in administrators and message.from_user.id not in Config.ADMINS:
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(base64.b32decode('====QCSTCHIOXXZJAR3SWXJJ'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8'))]
            ])
            await client.send_message(
                chat_id=message.chat.id,
                text=base64.b32decode('6RY6C6QR5UYBCSVM2L2EXXBNUL5CGQQOPT3ASSJOBDIKXXFPABLSHZJOP3U4DRRH'[::-1].encode('utf-8')).decode('utf-8'),
                reply_markup=reply_markup
            )
            return
    else:
        # Handle unauthorized users in a private chat
        if message.from_user.id not in Config.ADMINS:
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(base64.b32decode('====QCSTCHIOXXZJAR3SWXJJ'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8'))]
            ])
            await client.send_message(
                chat_id=message.chat.id,
                text=base64.b32decode('6RY6C6QR5UYBCSVM2L2EXXBNUL5CGQQOPT3ASSJOBDIKXXFPABLSHZJOP3U4DRRH'[::-1].encode('utf-8')).decode('utf-8'),
                reply_markup=reply_markup
            )
            return

    if not Config.CALL_STATUS:
        await message.reply_text(
            "<b>Player is idle, start the player using the button below.</b>",
            disable_web_page_preview=True,
            quote=False,
            reply_markup=await get_buttons()
        )
        return

    data = Config.DATA.get('FILE_DATA')
    k = await message.reply("<b>Trying to seek the music...</b>", quote=False)
    if not data.get('dur', 0) or data.get('dur') == 0:
        await k.edit("<b>Bruh! This stream can't be seeked.</b>")
        return

    if ' ' in message.text:
        _, time = message.text.split(" ")
        try:
            time = int(time)
        except ValueError:
            await k.edit('<b>Fuker Invalid time specified</b>')
            return

        nyav, string = await seek_file(time)
        if not nyav:
            await k.edit(string)
            return

        # Constructing title based on the current stream
        title = construct_title(data, Config)

        if Config.msg.get('player'):
            await Config.msg['player'].delete()
        Config.msg['player'] = await k.edit(f"🎸{title}", reply_markup=await get_buttons(), disable_web_page_preview=True)
    else:
        await k.edit('<b>Shit! No time specified</b>')

def construct_title(data, Config):
    if not data.get('dur', 0) or data.get('dur') == 0:
        return "<b>Playing Live Stream 🎸</b> ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ"
    elif Config.playlist:
        return f"<b>{Config.playlist[0][1]}</b>\nㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ"
    elif Config.STREAM_LINK:
        return f"<b>Stream Using [Url]({data['file']})</b> ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ"
    else:
        return f"<b>Streaming Startup [stream]({Config.STREAM_URL})</b> ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ"


@Client.on_message(filters.command(["settings", f"settings@{Config.BOT_USERNAME}"]))
async def settings(client, message):
    # Check if the command is used in a group chat
    if message.chat.type != enums.ChatType.PRIVATE:
        # Check if the command is used in the authorized chat
        if message.chat.id != Config.CHAT:
            buttons = [
                [
                    InlineKeyboardButton(base64.b32decode('====A25NCCI4W35JAJZWWQVJARFJ2PC6'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('======IOFL6CGWBKDSVIHZFMN3U6S4FMSL54WZFNC3L2WXNMORYKHUROJ3Z6SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8')),
                    InlineKeyboardButton(base64.b32decode('===KGZVMICI4WU5NKCIKIOK4'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8')),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await message.reply(
                "This is not the group which I have been configured to play in. Do you want to set this group as default CHAT?",
                quote=False,
                reply_markup=reply_markup
            )
            return

        administrators = []
        async for member in client.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            administrators.append(member.user.id)

        # Check if the user is an admin or in the Config.ADMINS list
        if message.from_user.id not in administrators and message.from_user.id not in Config.ADMINS:
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(base64.b32decode('====QCSTCHIOXXZJAR3SWXJJ'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8'))]
            ])
            await client.send_message(
                chat_id=message.chat.id,
                text=base64.b32decode('6RY6C6QR5UYBCSVM2L2EXXBNUL5CGQQOPT3ASSJOBDIKXXFPABLSHZJOP3U4DRRH'[::-1].encode('utf-8')).decode('utf-8'),
                reply_markup=reply_markup
            )
            return
    else:
        # Handle unauthorized users in a private chat
        if message.from_user.id not in Config.ADMINS:
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(base64.b32decode('====QCSTCHIOXXZJAR3SWXJJ'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8'))]
            ])
            await client.send_message(
                chat_id=message.chat.id,
                text=base64.b32decode('6RY6C6QR5UYBCSVM2L2EXXBNUL5CGQQOPT3ASSJOBDIKXXFPABLSHZJOP3U4DRRH'[::-1].encode('utf-8')).decode('utf-8'),
                reply_markup=reply_markup
            )
            return

    # Proceed with the settings function if the user is authorized
    await message.reply("<b>Configure Your VCPlayer Settings Here.</b>", reply_markup=await settings_panel(), disable_web_page_preview=True, quote=False)
    
    # Corrected the variable name from 'm' to 'message'
    await delete_messages([message])

