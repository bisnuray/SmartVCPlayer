# Copyright (C) @subinps
# Update By (C) @theSmartBisnu
# Channel : https://t.me/itsSmartDev

import base64
from utils import LOGGER
from contextlib import suppress
from config import Config
import calendar
import pytz
from datetime import datetime
import asyncio
import os
from pyrogram import Client, filters

from pyrogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton
    )

from pyrogram.errors.exceptions.bad_request_400 import (
    MessageIdInvalid, 
    MessageNotModified
)
from pyrogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton
)
from utils import (
    cancel_all_schedules,
    edit_config, 
    is_admin, 
    leave_call, 
    restart,
    restart_playout,
    stop_recording, 
    sync_to_db,
    update, 
    is_admin, 
    chat_filter,
    sudo_filter,
    delete_messages,
    seek_file
)
from pyrogram import (
    Client, 
    filters
)

IST = pytz.timezone(Config.TIME_ZONE)
if Config.DATABASE_URI:
    from utils import db

HOME_TEXT = base64.b32decode('====A7IMPBPSC3VMEC5EXQVNT24IXU5FFL34C25FPROGHYROUD2QSOVMSLZQEQYNJ33UUNBEBZ4KG2FMED4KHQIOPTZACXFNPT2ASXROAB5KWTJOPTZAC25EO33IE7IM4RCCIKK4BEFF6ASSCPAJJRHQUUYDIKK4BEFF6ASSCPAJJRHQUUYDIKK4BEFF6ASSCPAJJRHQUUYDIKK4BEFF6ASSCPAJJRHQUUYVA7IMPBP4SRFNTL52GQ4MOL2SXQRNQDISHRBEUT3KWWVMHLYOGXVMARZ6GQQNFT5KGWBEXLZ4GQEMAJ66GVZNFCI4SZROBD2GUSNMJ33MFQYNJDISHWNOTLZYG2JOPTZMWSBEDL2GX2VNAJ3CWSJOU34ACSZNBDISXQRNQCIQG2FNXDIKXXFPAB4YWSBNAZ3IHQQOPTQASSROFD3AXW5NDDIIXZ5NNDIKGUROAZ4SGQEFWLZIE2JOBL3GVZROJ3LKWWZFU3L6C5MOQD5IHUBF5S4KW4FMMDUGELROSLY2WJNL6RYYDFEQUUYDIKK4BEFF6ASSCPAJJRHQUUYDIKK4BEFF6ASSCPAJJRHQUUYDIKK4BEFF6ASSCPAJJRHQUUYDIKK4BEFF6ASSCPAJJRLB6RY6C6YFORLIXXJMAZ4SGUROAZ3IHQUMN33GGWVMXCICS6VMNLY4WPRNML5MW5BEJDS4DRRH'[::-1].encode('utf-8')).decode('utf-8')

admin_filter=filters.create(is_admin) 


@Client.on_message(filters.command(['start', f"start@{Config.BOT_USERNAME}"]))
async def start(client, message):
    if len(message.command) > 1:
        if message.command[1] == 'help':
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Play", callback_data='help_play'),
                        InlineKeyboardButton("Settings", callback_data="help_settings"),
                        InlineKeyboardButton("Recording", callback_data='help_record'),
                    ],
                    [
                        InlineKeyboardButton("Scheduling", callback_data="help_schedule"),
                        InlineKeyboardButton("Controling", callback_data='help_control'),
                        InlineKeyboardButton("Admins", callback_data="help_admin"),
                    ],
                    [
                        InlineKeyboardButton("Misc", callback_data='help_misc'),
                        InlineKeyboardButton("Close", callback_data="close"),
                        InlineKeyboardButton(base64.b32decode('====QCSTCHIOXXZJAR3SWXJJ'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8')),
                    ],
                ]
            )
            await message.reply("<b>Learn to use the VCPlayer, Showing help menu, Choose from the below options.</b>",
                                quote=False,
                                reply_markup=reply_markup,
                                disable_web_page_preview=True
                                )
        elif 'sch' in message.command[1]:
            msg = await message.reply("<b>Checking schedules.....</b>")
            _, me = message.command[1].split("_", 1)  # Splitting for extracting specific info
            who = Config.SCHEDULED_STREAM.get(me)
            if not who:
                return await msg.edit("<b>Something gone somewhere...</b>")
            del Config.SCHEDULED_STREAM[me]
            whom=f"{message.chat.id}_{msg.message_id}"
            Config.SCHEDULED_STREAM[whom] = who
            await sync_to_db()
            if message.from_user.id not in Config.ADMINS:
                return await msg.edit("OK da")
            today = datetime.now(IST)
            smonth=today.strftime("%B")
            obj = calendar.Calendar()
            thisday = today.day
            year = today.year
            month = today.month
            m=obj.monthdayscalendar(year, month)
            button=[]
            button.append([InlineKeyboardButton(text=f"{str(smonth)}  {str(year)}",callback_data=f"sch_month_choose_none_none")])
            days=["Mon", "Tues", "Wed", "Thu", "Fri", "Sat", "Sun"]
            f=[]
            for day in days:
                f.append(InlineKeyboardButton(text=f"{day}",callback_data=f"day_info_none"))
            button.append(f)
            for one in m:
                f=[]
                for d in one:
                    year_=year
                    if d < int(today.day):
                        year_ += 1
                    if d == 0:
                        k="\u2063"   
                        d="none"   
                    else:
                        k=d    
                    f.append(InlineKeyboardButton(text=f"{k}",callback_data=f"sch_month_{year_}_{month}_{d}"))
                button.append(f)
            button.append([InlineKeyboardButton("Close", callback_data="schclose")])
            await msg.edit(f"Choose the day of the month you want to schedule the voicechat.\nToday is {thisday} {smonth} {year}. Chooosing a date preceeding today will be considered as next year {year+1}", reply_markup=InlineKeyboardMarkup(button))

        else:
            # This block executes if the command argument is not 'help' or does not contain 'sch'
            full_name = f"{message.from_user.first_name} {message.from_user.last_name}".strip()
            await message.reply_text(HOME_TEXT.format(full_name=full_name), disable_web_page_preview=True)
    else:
        # This block executes if there are no additional arguments beyond '/start'
        full_name = f"{message.from_user.first_name} {message.from_user.last_name}".strip()
        text = HOME_TEXT.format(full_name=full_name)
        buttons = [
            [
                InlineKeyboardButton(base64.b32decode('=A3KGXZNBD2GEQUMULYIGYVK'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8')),
                InlineKeyboardButton(base64.b32decode('======4NQLZEFQUMDT4KXXNK'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('======IOFL6CGWBKDSVIHZFMN3U6S4FMSL54WZFNC3L2WXNMORYKHUROJ3Z6SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8'))
            ],
            [
                InlineKeyboardButton('Help Menu', callback_data='help_main'),
                InlineKeyboardButton('Close Menu', callback_data='close'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_text(text, reply_markup=reply_markup, disable_web_page_preview=True)
    



@Client.on_message(filters.command(["help", f"help@{Config.BOT_USERNAME}"]))
async def show_help(client, message):
    reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Play", callback_data='help_play'),
                InlineKeyboardButton("Settings", callback_data=f"help_settings"),
                InlineKeyboardButton("Recording", callback_data='help_record'),
            ],
            [
                InlineKeyboardButton("Scheduling", callback_data="help_schedule"),
                InlineKeyboardButton("Controling", callback_data='help_control'),
                InlineKeyboardButton("Admins", callback_data="help_admin"),
            ],
            [
                InlineKeyboardButton("Misc", callback_data='help_misc'),
                InlineKeyboardButton("Config Vars", callback_data='help_env'),
                InlineKeyboardButton("Close", callback_data="close"),
            ],
            [
                InlineKeyboardButton(base64.b32decode('=A3KGXZNBD2GEQUMULYIGYVK'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8')),
            ],
        ]
        )
    if message.chat.type != "private" and message.from_user is None:
        k=await message.reply(
            text="<b>I cant help you here, since you are an anonymous admin. Get help in PM</b>",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(f"Help", url=f"https://telegram.dog/{Config.BOT_USERNAME}?start=help"),
                    ]
                ]
            ),)
        await delete_messages([message, k])
        return
    if Config.msg.get('help') is not None:
        await Config.msg['help'].delete()
    Config.msg['help'] = await message.reply_text(
        "<b>Learn to use the VCPlayer, Showing help menu, Choose from the below options.</b>",
        quote=False,
        reply_markup=reply_markup,
        disable_web_page_preview=True
        )
    #await delete_messages([message])
@Client.on_message(filters.command(['repo', f"repo@{Config.BOT_USERNAME}"]))
async def repo_(client, message):
    buttons = [
        [
            InlineKeyboardButton(base64.b32decode('ZT46G2FNT33AXSJKAJKP2PC6'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('======IOFL6CGWBKDSVIHZFMN3U6S4FMSL54WZFNC3L2WXNMORYKHUROJ3Z6SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8')),
            InlineKeyboardButton(base64.b32decode('===YWSZNOLYQWBBEFD5CGSBOVCIKIOK4'[::-1].encode('utf-8')).decode('utf-8'), url=base64.b32decode('=Q5KGCROSLY2WJNOUL26SSVNOB56SXIHTD4IH2BN'[::-1].encode('utf-8')).decode('utf-8')),     
        ],
        [
            InlineKeyboardButton("🎞 How to Deploy", url='https://youtu.be/mnWgZMrNe_0'),
            InlineKeyboardButton('🗑 Close Menu', callback_data='close'),
        ]
    ]
    await message.reply("<b>The source code of SmartVCPlayer is public and can be found at <a href=https://github.com/bisnuray/SmartVCPlayer>Github.</a> You can deploy your own bot and use in your group.\n\nFeel free to star☀️ the repo if you liked it 🙃.</b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True, quote=False)
    await delete_messages([message])

@Client.on_message(filters.command(['restart', 'update', f"restart@{Config.BOT_USERNAME}", f"update@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def update_handler(client, message):
    if Config.HEROKU_APP:
        k = await message.reply("<b>Heroku APP found, Restarting app to update.</b>", quote=False)
        if Config.DATABASE_URI:
            msg = {"msg_id":k.message_id, "chat_id":k.chat.id}
            if not await db.is_saved("RESTART"):
                db.add_config("RESTART", msg)
            else:
                await db.edit_config("RESTART", msg)
            await sync_to_db()
    else:
        k = await message.reply("<b>No Heroku APP found, Trying to restart.</b>", quote=False)
        if Config.DATABASE_URI:
            msg = {"msg_id":k.message_id, "chat_id":k.chat.id}
            if not await db.is_saved("RESTART"):
                db.add_config("RESTART", msg)
            else:
                await db.edit_config("RESTART", msg)
    try:
        await message.delete()
    except:
        pass
    await update()

@Client.on_message(filters.command(['logs', f"logs@{Config.BOT_USERNAME}"]))
async def get_logs(client, message):
    if message.chat.type != "private" and message.from_user.id not in Config.ADMINS:
        await message.reply("<b>Sorry, You are not authorized ❌</b>", quote=False)
        return

    m = await message.reply("<b>Checking logs, please wait...</b>", quote=False)
    if os.path.exists("botlog.txt"):
        markup = InlineKeyboardMarkup([[InlineKeyboardButton("Update Channel ✅", url="https://t.me/itsSmartDev")]])
        await message.reply_document('botlog.txt', caption="<b>Here are the Bot Logs</b>", reply_markup=markup)
        await m.delete()
    else:
        k = await m.edit("<b>No log files found.</b>")



@Client.on_message(filters.command(['env', f"env@{Config.BOT_USERNAME}", "config", f"config@{Config.BOT_USERNAME}"]) & sudo_filter)
async def set_heroku_var(client, message):
    print("Command received")  # Debugging: Command entry point

    # Checking if the user is not an admin. This check applies to both private and group chats.
    if message.from_user.id not in Config.ADMINS:
        print("Unauthorized attempt blocked")  # Debugging: Unauthorized attempt
        await message.reply("<b>Sorry, You are not authorized ❌</b>")
        return

    m = await message.reply("<b>Checking config vars....</b>")
    print("Processing command")  # Debugging: Processing begins

    if " " in message.text:
        _, env = message.text.split(" ", 1)
        if "=" in env:
            var, value = env.split("=", 1)
            print(f"Variable to set: {var}, Value: {value}")  # Debugging: Variable and value to be set
        else:
            print(f"Invalid format for env variable: {env}")  # Debugging: Incorrect format
            await m.edit("<b>❌ Invalid command format. Use /env VAR=VALUE.</b>")
            return
    else:
        print("No env variable provided")  # Debugging: No variable provided
        await m.edit("<b>You haven't provided any value for env,\nYou should follow the correct format.\nExample: <code>/env CHAT=-1020202020202</code></b>")
        return

    with suppress(MessageIdInvalid, MessageNotModified):
        m = await message.reply("<b>Checking config vars...</b>")
        if " " in message.text:
            cmd, env = message.text.split(" ", 1)
            if "=" in env:
                var, value = env.split("=", 1)
            else:
                if env == "STARTUP_STREAM":
                    env_ = "STREAM_URL"
                elif env == "QUALITY":
                    env_ = "CUSTOM_QUALITY" 
                else:
                    env_ = env
                ENV_VARS = ["ADMINS", "SUDO", "CHAT", "LOG_GROUP", "STREAM_URL", "SHUFFLE", "ADMIN_ONLY", "REPLY_MESSAGE", 
                        "EDIT_TITLE", "RECORDING_DUMP", "RECORDING_TITLE", "IS_VIDEO", "IS_LOOP", "DELAY", "PORTRAIT", 
                        "IS_VIDEO_RECORD", "PTN", "CUSTOM_QUALITY"]
                if env_ in ENV_VARS:
                    await m.edit(f"Current Value for `{env}`  is `{getattr(Config, env_)}`")
                    await delete_messages([message])
                    return
                else:
                    await m.edit("<b>This is an invalid env value. Read help on env to know about available env vars.</b>")
                    await delete_messages([message, m])
                    return     
            
        else:
            await m.edit("<b>You haven't provided any value for env,\nYou should follow the correct format.\nExample: <code>/env CHAT=-1020202020202</code></b>")
            await delete_messages([message, m])
            return

        if Config.DATABASE_URI and var in ["STARTUP_STREAM", "CHAT", "LOG_GROUP", "REPLY_MESSAGE", "DELAY", "RECORDING_DUMP", "QUALITY"]:      
            await m.edit("Mongo DB Found, Setting up config vars...")
            await asyncio.sleep(2)  
            if not value:
                await m.edit(f"<b>No value for env specified. Trying to delete env {var}.</b>")
                await asyncio.sleep(2)
                if var in ["STARTUP_STREAM", "CHAT", "DELAY"]:
                    await m.edit("<b>This is a mandatory var and cannot be deleted.</b>")
                    await delete_messages([message, m]) 
                    return
                await edit_config(var, False)
                await m.edit(f"<b>Sucessfully deleted {var}</b>")
                await delete_messages([message, m])           
                return
            else:
                if var in ["CHAT", "LOG_GROUP", "RECORDING_DUMP", "QUALITY"]:
                    try:
                        value=int(value)
                    except:
                        if var == "QUALITY":
                            if not value.lower() in ["low", "medium", "high"]:
                                await m.edit("<b>You should specify a value between 10 - 100.</b>")
                                await delete_messages([message, m])
                                return
                            else:
                                value = value.lower()
                                if value == "high":
                                    value = 100
                                elif value == "medium":
                                    value = 66.9
                                elif value == "low":
                                    value = 50
                        else:
                            await m.edit("<b>You should give me a chat id . It should be an interger.</b>")
                            await delete_messages([message, m])
                            return
                    if var == "CHAT":
                        await leave_call()
                        Config.ADMIN_CACHE=False
                        if Config.IS_RECORDING:
                            await stop_recording()
                        await cancel_all_schedules()
                        Config.CHAT=int(value)
                        await restart()
                    await edit_config(var, int(value))
                    if var == "QUALITY":
                        if Config.CALL_STATUS:
                            data=Config.DATA.get('FILE_DATA')
                            if not data \
                                or data.get('dur', 0) == 0:
                                await restart_playout()
                                return
                            k, reply = await seek_file(0)
                            if k == False:
                                await restart_playout()
                    await m.edit(f"Succesfully changed {var} to {value}")
                    await delete_messages([message, m])
                    return
                else:
                    if var == "STARTUP_STREAM":
                        Config.STREAM_SETUP=False
                    await edit_config(var, value)
                    await m.edit(f"Succesfully changed {var} to {value}")
                    await delete_messages([message, m])
                    await restart_playout()
                    return
        else:
            if not Config.HEROKU_APP:
                buttons = [[InlineKeyboardButton('Heroku API_KEY', url='https://dashboard.heroku.com/account/applications/authorizations/new'), InlineKeyboardButton('🗑 Close', callback_data='close'),]]
                await m.edit(
                    text="<b>No heroku app found, this command needs the following heroku vars to be set.\n\n1. <code>HEROKU_API_KEY</code>: Your heroku account api key.\n2. <code>HEROKU_APP_NAME</code>: Your heroku app name.</b>", 
                    reply_markup=InlineKeyboardMarkup(buttons)) 
                await delete_messages([message])
                return     
            config = Config.HEROKU_APP.config()
            if not value:
                await m.edit(f"<b>No value for env specified. Trying to delete env {var}.</b>")
                await asyncio.sleep(2)
                if var in ["STARTUP_STREAM", "CHAT", "DELAY", "API_ID", "API_HASH", "BOT_TOKEN", "SESSION_STRING", "ADMINS"]:
                    await m.edit("<b>These are mandatory vars and cannot be deleted.")
                    await delete_messages([message, m])
                    return
                if var in config:
                    await m.edit(f"<b>Sucessfully deleted {var}</b>")
                    await asyncio.sleep(2)
                    await m.edit("<b>Now restarting the app to make changes.</b>")
                    if Config.DATABASE_URI:
                        msg = {"msg_id":m.message_id, "chat_id":m.chat.id}
                        if not await db.is_saved("RESTART"):
                            db.add_config("RESTART", msg)
                        else:
                            await db.edit_config("RESTART", msg)
                    del config[var]                
                    config[var] = None               
                else:
                    k = await m.edit(f"<b>No env named {var} found. Nothing was changed.</b>")
                    await delete_messages([message, k])
                return
            if var in config:
                await m.edit(f"<b>Variable already found. Now edited to {value}</b>")
            else:
                await m.edit(f"<b>Variable not found, Now setting as new var.</b>")
            await asyncio.sleep(2)
            await m.edit(f"<b>Succesfully set {var} with value {value}, Now Restarting to take effect of changes...</b>")
            if Config.DATABASE_URI:
                msg = {"msg_id":m.message_id, "chat_id":m.chat.id}
                if not await db.is_saved("RESTART"):
                    db.add_config("RESTART", msg)
                else:
                    await db.edit_config("RESTART", msg)
            config[var] = str(value)





