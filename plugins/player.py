# Copyright (C) @subinps
# Update By (C) @theSmartBisnu
# Channel : https://t.me/itsSmartDev

from utils import LOGGER
from youtube_search import YoutubeSearch
from contextlib import suppress
from pyrogram.types import Message
from yt_dlp import YoutubeDL
from datetime import datetime
from pyrogram import filters, enums
from config import Config
from PTN import parse
import re
from utils import (
    add_to_db_playlist, 
    clear_db_playlist, 
    delete_messages, 
    download, 
    get_admins, 
    get_duration,
    is_admin, 
    get_buttons, 
    get_link, 
    import_play_list, 
    is_audio, 
    leave_call, 
    play, 
    get_playlist_str, 
    send_playlist, 
    shuffle_playlist, 
    start_stream, 
    stream_from_link, 
    chat_filter,
    c_play,
    is_ytdl_supported
)
from pyrogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton
    )
from pyrogram.errors import (
    MessageIdInvalid, 
    MessageNotModified,
    UserNotParticipant,
    PeerIdInvalid,
    ChannelInvalid
    )
from pyrogram import (
    Client, 
    filters
    )


admin_filter=filters.create(is_admin) 

@Client.on_message(filters.command(["play", "fplay", f"play@{Config.BOT_USERNAME}", f"fplay@{Config.BOT_USERNAME}"]))
async def add_to_playlist(client, message):
    print(f"Command received from {message.from_user.id} in chat type: {message.chat.type}")
    with suppress(MessageIdInvalid, MessageNotModified):
        # Check if the command is used in the authorized chat
        if message.chat.id != Config.CHAT and message.chat.type != enums.ChatType.PRIVATE:
            buttons = [
                [
                    InlineKeyboardButton('🤖 Make Own Bot', url='https://github.com/bisnuray/SmartVCPlayer'),
                    InlineKeyboardButton('✅ Join Here', url='https://t.me/itsSmartDev'),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await message.reply(
                "This is not the group which I have been configured to play in. Do you want to set this group as default CHAT?",
                quote=False,
                reply_markup=reply_markup
            )
            return
        
        # Fetch the list of admins for the chat
        admins = await get_admins(Config.CHAT)

        # Check if the command is restricted to admins only
        if Config.ADMIN_ONLY:
            # Check if the user is an admin or the message is sent via a channel
            if not (message.from_user is None and message.sender_chat or message.from_user.id in admins):
                # User is not authorized to use the command
                await message.reply("<b>Sorry! You are not authorized ❌</b>", quote=False)
                return
        type=""
        yturl=""
        ysearch=""
        url=""
        if message.command[0] == "fplay":
            if not (message.from_user is None and message.sender_chat or message.from_user.id in admins):
                k=await message.reply("This command is only for admins.", quote=False)
                await delete_messages([message, k])
                return
        msg = await message.reply_text("⚡️ **Checking recived input..**", quote=False)
        if message.reply_to_message and message.reply_to_message.video:
            await msg.edit("⚡️ **Checking Telegram Media...**")
            type='video'
            m_video = message.reply_to_message.video       
        elif message.reply_to_message and message.reply_to_message.document:
            await msg.edit("⚡️ **Checking Telegram Media...**")
            m_video = message.reply_to_message.document
            type='video'
            if not "video" in m_video.mime_type:
                return await msg.edit("The given file is invalid")
        elif message.reply_to_message and message.reply_to_message.audio:
            #if not Config.IS_VIDEO:
                #return await message.reply("Play from audio file is available only if Video Mode if turned off.\nUse /settings to configure ypur player.")
            await msg.edit("⚡️ **Checking Telegram Media...**")
            type='audio'
            m_video = message.reply_to_message.audio       
        else:
            if message.reply_to_message and message.reply_to_message.text:
                query=message.reply_to_message.text
            elif " " in message.text:
                text = message.text.split(" ", 1)
                query = text[1]
            else:
                await msg.edit("<b>You Didn't gave me anything to play.</b>")
                await delete_messages([message, msg])
                return
            regex = r"^(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\-_]+)\&?"
            match = re.match(regex,query)
            if match:
                type="youtube"
                yturl=query
            elif query.startswith("http"):
                try:
                    has_audio_ = await is_audio(query)
                except:
                    has_audio_ = False
                    LOGGER.error("Unable to get Audio properties within time.")
                if has_audio_:
                    try:
                        dur=await get_duration(query)
                    except:
                        dur=0
                    if dur == 0:
                        await msg.edit("<b>This is a live stream, Use /stream command.</b>")
                        await delete_messages([message, msg])
                        return 
                    type="direct"
                    url=query
                else:
                    if is_ytdl_supported(query):
                        type="ytdl_s"
                        url=query
                    else:
                        await msg.edit("<b>Invalid link ❌ , provide me a direct link or a youtube link.</b>")
                        await delete_messages([message, msg])
                        return
            else:
                type="query"
                ysearch=query
        if not message.from_user is None:
            user=f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
            user_id = message.from_user.id
        else:
            user="Anonymous 👻"
            user_id = "anonymous_admin"
        now = datetime.now()
        nyav = now.strftime("%d-%m-%Y-%H:%M:%S")
        if type in ["video", "audio"]:
            if type == "audio":
                if m_video.title is None:
                    if m_video.file_name is None:
                        title_ = "Music"
                    else:
                        title_ = m_video.file_name
                else:
                    title_ = m_video.title
                if m_video.performer is not None:
                    title = f"{m_video.performer} - {title_}"
                else:
                    title=title_
                unique = f"{nyav}_{m_video.file_size}_audio"
            else:
                title=m_video.file_name
                unique = f"{nyav}_{m_video.file_size}_video"
                if Config.PTN:
                    ny = parse(title)
                    title_ = ny.get("title")
                    if title_:
                        title = title_
            file_id=m_video.file_id
            if title is None:
                title = 'Music'
            data={1:title, 2:file_id, 3:"telegram", 4:user, 5:unique}
            if message.command[0] == "fplay":
                pla = [data] + Config.playlist
                Config.playlist = pla
            else:
                Config.playlist.append(data)
            await add_to_db_playlist(data)        
            await msg.edit("<b>Media added to playlist ✅</b>")
        elif type in ["youtube", "query", "ytdl_s"]:
            if type=="youtube":
                await msg.edit("⚡️ **Fetching Video From YouTube...**")
                url=yturl
            elif type=="query":
                try:
                    await msg.edit("⚡️ **Fetching Video From YouTube...**")
                    ytquery=ysearch
                    results = YoutubeSearch(ytquery, max_results=1).to_dict()
                    url = f"https://youtube.com{results[0]['url_suffix']}"
                    title = results[0]["title"][:40]
                except Exception as e:
                    await msg.edit(
                        "<b>Song not found.\nTry inline mode...</b>"
                    )
                    LOGGER.error(str(e), exc_info=True)
                    await delete_messages([message, msg])
                    return
            elif type == "ytdl_s":
                url=url
            else:
                return
            ydl_opts = {
                "quite": True,
                "geo-bypass": True,
                "nocheckcertificate": True
            }
            ydl = YoutubeDL(ydl_opts)
            try:
                info = ydl.extract_info(url, False)
            except Exception as e:
                LOGGER.error(e, exc_info=True)
                await msg.edit(
                    f"<b>YouTube Download Error ❌\nError:- {e}</b>"
                    )
                LOGGER.error(str(e))
                await delete_messages([message, msg])
                return
            if type == "ytdl_s":
                title = "Music"
                try:
                    title = info['title']
                except:
                    pass
            else:
                title = info["title"]
                if info['duration'] is None:
                    await msg.edit("<b>This is a live stream, Use /stream command.</b>")
                    await delete_messages([message, msg])
                    return 
            data={1:title, 2:url, 3:"youtube", 4:user, 5:f"{nyav}_{user_id}"}
            if message.command[0] == "fplay":
                pla = [data] + Config.playlist
                Config.playlist = pla
            else:
                Config.playlist.append(data)
            await add_to_db_playlist(data)
            await msg.edit(f"<b>[{title}]({url}) added to playist</b>", disable_web_page_preview=True)
        elif type == "direct":
            data={1:"Music", 2:url, 3:"url", 4:user, 5:f"{nyav}_{user_id}"}
            if message.command[0] == "fplay":
                pla = [data] + Config.playlist
                Config.playlist = pla
            else:
                Config.playlist.append(data)
            await add_to_db_playlist(data)        
            await msg.edit("<b>Link added to playlist ✅</b>")
        if not Config.CALL_STATUS \
            and len(Config.playlist) >= 1:
            await msg.edit("<b>Downloading and Processing...</b>")
            await download(Config.playlist[0], msg)
            await play()
        elif (len(Config.playlist) == 1 and Config.CALL_STATUS):
            await msg.edit("<b>Downloading and Processing...</b>")
            await download(Config.playlist[0], msg)  
            await play()
        elif message.command[0] == "fplay":
            await msg.edit("<b>Downloading and Processing...</b>")
            await download(Config.playlist[0], msg)  
            await play()
        
        else:
            await send_playlist()  
        await msg.delete()
        pl=await get_playlist_str()
        if message.chat.type == enums.ChatType.PRIVATE:
            await message.reply(pl, reply_markup=await get_buttons() ,disable_web_page_preview=True)       
        elif message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            if Config.msg.get('playlist') is not None:
                await Config.msg['playlist'].delete()
                Config.msg['playlist']=await message.reply(pl, disable_web_page_preview=True, reply_markup=await get_buttons())    
            await delete_messages([message])  
        for track in Config.playlist[:2]:
            await download(track)
        

@Client.on_message(filters.command(["leave", f"leave@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def leave_voice_chat(_, m: Message):
    if not Config.CALL_STATUS:        
        k=await m.reply("<b>Not joined any voicechat.</b>", quote=False)
        await delete_messages([m, k])
        return
    await leave_call()
    k=await m.reply("<b>Succesfully left videochat.</b>", quote=False)
    await delete_messages([m, k])



@Client.on_message(filters.command(["shuffle", f"shuffle@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def shuffle_play_list(client, m: Message):
    if not Config.CALL_STATUS:
        k = await m.reply("<b>Not joined any voicechat.</b>", quote=False)
        await delete_messages([m, k])
        return
    else:
        if len(Config.playlist) > 2:
            k=await m.reply_text(f"Playlist Shuffled.", quote=False)
            await shuffle_playlist()
            await delete_messages([m, k])            
        else:
            k=await m.reply_text(f"You cant shuffle playlist with less than 3 songs.", quote=False)
            await delete_messages([m, k])


@Client.on_message(filters.command(["clearplaylist", f"clearplaylist@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def clear_play_list(client, m: Message):
    if not Config.playlist:
        k = await m.reply("<b>Bruh! Playlist is empty 🤷‍♂️</b>", quote=False)  
        await delete_messages([m, k])
        return
    Config.playlist.clear()
    k=await m.reply_text(f"<b>Music Playlist Cleared ✅</b>", quote=False)
    await clear_db_playlist(all=True)
    if Config.IS_LOOP \
        and not (Config.YPLAY or Config.CPLAY):
        await start_stream()
    else:
        await leave_call()
    await delete_messages([m, k])



@Client.on_message(filters.command(["cplay", f"cplay@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def channel_play_list(client, m: Message):
    with suppress(MessageIdInvalid, MessageNotModified):
        k=await m.reply("<b>Setting up for channel play...</b>", quote=False)
        if " " in m.text:
            you, me = m.text.split(" ", 1)
            if me.startswith("-100"):
                try:
                    me=int(me)
                except:
                    await k.edit("<b>Invalid chat id given</b>", quote=False)
                    await delete_messages([m, k])
                    return
                try:
                    await client.get_chat_member(int(me), Config.USER_ID)
                except (ValueError, PeerIdInvalid, ChannelInvalid):
                    LOGGER.error(f"Given channel is private and @{Config.BOT_USERNAME} is not an admin over there.", exc_info=True)
                    await k.edit(f"Given channel is private and @{Config.BOT_USERNAME} is not an admin over there. If channel is not private , please provide username of channel.")
                    await delete_messages([m, k])
                    return
                except UserNotParticipant:
                    LOGGER.error("Given channel is private and USER account is not a member of channel.")
                    await k.edit("Given channel is private and USER account is not a member of channel.")
                    await delete_messages([m, k])
                    return
                except Exception as e:
                    LOGGER.error(f"Errors occured while getting data abount channel - {e}", exc_info=True)
                    await k.edit(f"Something went wrong- {e}")
                    await delete_messages([m, k])
                    return
                await k.edit("Searching files from channel, this may take some time, depending on number of files in the channel.")
                st, msg = await c_play(me)
                if st == False:
                    await m.edit(msg)
                else:
                    await k.edit(f"Succesfully added {msg} files to playlist.")
            elif me.startswith("@"):
                me = me.replace("@", "")
                try:
                    chat=await client.get_chat(me)
                except Exception as e:
                    LOGGER.error(f"Errors occured while fetching info about channel - {e}", exc_info=True)
                    await k.edit(f"Errors occured while getting data about channel - {e}")
                    await delete_messages([m, k])
                    return
                await k.edit("Searching files from channel, this may take some time, depending on number of files in the channel.")
                st, msg=await c_play(me)
                if st == False:
                    await k.edit(msg)
                    await delete_messages([m, k])
                else:
                    await k.edit(f"Succesfully Added {msg} files from {chat.title} to playlist")
                    await delete_messages([m, k])
            else:
                await k.edit("The given channel is invalid. For private channels it should start with -100 and for public channels it should start with @\nExamples - `/cplay @VCPlayerFiles or /cplay -100125369865\n\nFor private channel, both bot and the USER account should be members of channel.")
                await delete_messages([m, k])
        else:
            await k.edit("You didn't gave me any channel. Give me a channel id or username from which i should play files . \nFor private channels it should start with -100 and for public channels it should start with @\nExamples - `/cplay @VCPlayerFiles or /cplay -100125369865\n\nFor private channel, both bot and the USER account should be members of channel.")
            await delete_messages([m, k])



@Client.on_message(filters.command(["yplay", f"yplay@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def yt_play_list(client, m: Message):
    with suppress(MessageIdInvalid, MessageNotModified):
        if m.reply_to_message is not None and m.reply_to_message.document:
            if m.reply_to_message.document.file_name != "YouTube_PlayList.json":
                k=await m.reply("Invalid PlayList file given. Use @GetPlayListBot  or search for a playlist in @DumpPlaylist to get a playlist file.")
                await delete_messages([m, k])
                return
            ytplaylist=await m.reply_to_message.download()
            status=await m.reply("Trying to get details from playlist.", quote=False)
            n=await import_play_list(ytplaylist)
            if not n:
                await status.edit("Errors Occured while importing playlist.", quote=False)
                await delete_messages([m, status])
                return
            if Config.SHUFFLE:
                await shuffle_playlist()
            pl=await get_playlist_str()
            if m.chat.type == "private":
                await status.edit(pl, disable_web_page_preview=True, reply_markup=await get_buttons())        
            elif not Config.LOG_GROUP and m.chat.type == "supergroup":
                if Config.msg.get("playlist") is not None:
                    await Config.msg['playlist'].delete()
                Config.msg['playlist']=await status.edit(pl, disable_web_page_preview=True, reply_markup=await get_buttons())
                await delete_messages([m])
            else:
                await delete_messages([m, status])
        else:
            k=await m.reply("No playList file given. Use @GetPlayListBot  or search for a playlist in @DumpPlaylist to get a playlist file.")
            await delete_messages([m, k])


@Client.on_message(filters.command(["stream", f"stream@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def stream(client, m: Message):
    with suppress(MessageIdInvalid, MessageNotModified):
        msg=await m.reply("<b>Checking the recived input.</b>", quote=False)
        if m.reply_to_message and m.reply_to_message.text:
            link=m.reply_to_message.text
        elif " " in m.text:
            text = m.text.split(" ", 1)
            link = text[1]
        else:
            k = await msg.edit("<b>Provide a link to stream!</b>")
            await delete_messages([m, k])
            return
        regex = r"^(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\-_]+)\&?"
        match = re.match(regex,link)
        if match:
            stream_link=await get_link(link)
            if not stream_link:
                k = await msg.edit("<b>This is an invalid link.</b>")
                await delete_messages([m, k])
                return
        else:
            stream_link=link
        try:
            is_audio_ = await is_audio(stream_link)
        except:
            is_audio_ = False
            LOGGER.error("Unable to get Audio properties within time.")
        if not is_audio_:
            k = await msg.edit("<b>This is an invalid link, provide me a direct link or a youtube link.</b>")
            await delete_messages([m, k])
            return
        try:
            dur=await get_duration(stream_link)
        except:
            dur=0
        if dur != 0:
            k = await msg.edit("<b>This is not a live stream, Use /play command.</b>")
            await delete_messages([m, k])
            return
        k, msg_=await stream_from_link(stream_link)
        if k == False:
            k = await msg.edit(msg_)
            await delete_messages([m, k])
            return
        if Config.msg.get('player'):
            await Config.msg['player'].delete()
        Config.msg['player']=await msg.edit(f"<b>🎸 [Streaming]({stream_link}) Started.</b>", disable_web_page_preview=True, reply_markup=await get_buttons())
        await delete_messages([m])
        


admincmds=["yplay", "leave", "pause", "resume", "skip", "restart", "volume", "shuffle", "clearplaylist", "export", "import", "update", 'replay', 'logs', 'stream', 'fplay', 'schedule', 'record', 'slist', 'cancel', 'cancelall', 'vcpromote', 'vcdemote', 'refresh', 'rtitle', 'seek', 'vcmute', 'unmute',
f'stream@{Config.BOT_USERNAME}', f'logs@{Config.BOT_USERNAME}', f"replay@{Config.BOT_USERNAME}", f"yplay@{Config.BOT_USERNAME}", f"leave@{Config.BOT_USERNAME}", f"pause@{Config.BOT_USERNAME}", f"resume@{Config.BOT_USERNAME}", f"skip@{Config.BOT_USERNAME}", 
f"restart@{Config.BOT_USERNAME}", f"volume@{Config.BOT_USERNAME}", f"shuffle@{Config.BOT_USERNAME}", f"clearplaylist@{Config.BOT_USERNAME}", f"export@{Config.BOT_USERNAME}", f"import@{Config.BOT_USERNAME}", f"update@{Config.BOT_USERNAME}",
f'play@{Config.BOT_USERNAME}', f'schedule@{Config.BOT_USERNAME}', f'record@{Config.BOT_USERNAME}', f'slist@{Config.BOT_USERNAME}', f'cancel@{Config.BOT_USERNAME}', f'cancelall@{Config.BOT_USERNAME}', f'vcpromote@{Config.BOT_USERNAME}', 
f'vcdemote@{Config.BOT_USERNAME}', f'refresh@{Config.BOT_USERNAME}', f'rtitle@{Config.BOT_USERNAME}', f'seek@{Config.BOT_USERNAME}', f'mute@{Config.BOT_USERNAME}', f'vcunmute@{Config.BOT_USERNAME}'
]

allcmd = ["play", "player", f"play@{Config.BOT_USERNAME}", f"player@{Config.BOT_USERNAME}"] + admincmds

@Client.on_message(filters.command(admincmds) & ~admin_filter & chat_filter)
async def notforu(_, m: Message):
    k = await _.send_message(
        chat_id=m.chat.id,
        text="<b>Sorry! You are not authorized ❌</b>",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Join Now ✅', url='https://t.me/itsSmartDev')]])
    )
    await delete_messages([m, k])



@Client.on_message(filters.command(allcmd) & ~chat_filter & filters.group)
async def not_chat(_, m: Message):
    if m.from_user is not None and m.from_user.id in Config.SUDO:
        buttons = [
            [
                InlineKeyboardButton('⚡️Change CHAT', callback_data='set_new_chat'),
            ],
            [
                InlineKeyboardButton('No', callback_data='closesudo'),
            ]
            ]
        await m.reply("This is not the group which i have been configured to play, Do you want to set this group as default CHAT?", quote=False, reply_markup=InlineKeyboardMarkup(buttons))
        await delete_messages([m])
    else:
        buttons = [
            [
                InlineKeyboardButton('⚡️Make Own Bot', url='https://github.com/bisnuray/SmartVCPlayer'),
                InlineKeyboardButton('✅ Join Here', url='https://t.me/itsSmartDev'),
            ]
            ]
        await m.reply("<b>You can't use this bot in this group, for that you have to make your own bot from the [SOURCE CODE](https://github.com/bisnuray/SmartVCPlayer) below.</b>", quote=False, disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(buttons))

