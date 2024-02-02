# Copyright (C) @subinps
# Update By (C) @theSmartBisnu
# Channel : https://t.me/itsSmartDev


from utils import LOGGER
from config import Config
from pyrogram import (
    Client, 
    filters
)
from utils import (
    chat_filter, 
    is_admin, 
    is_admin, 
    delete_messages, 
    recorder_settings,
    sync_to_db
)
from pyrogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton
)

admin_filter=filters.create(is_admin) 


@Client.on_message(filters.command(["record", f"record@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def record_vc(bot, message):
    await message.reply("Configure you VCPlayer Recording settings from here", reply_markup=(await recorder_settings()))
    await delete_messages([message])

@Client.on_message(filters.command(["rtitle", f"rtitle@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def recording_title(bot, message):
    m=await message.reply("Checking..")
    if " " in message.text:
        cmd, title = message.text.split(" ", 1)
    else:
        await m.edit("Give me a new title. Use /rtitle < Custom Title >\nUse <code>False</code> to revert to default title")
        await delete_messages([message, m])
        return

    if Config.DATABASE_URI:
        await m.edit("Mongo DB Found, Setting up recording title...") 
        if title == "False":
            await m.edit(f"Sucessfully removed custom recording title.")
            Config.RECORDING_TITLE=False
            await sync_to_db()
            await delete_messages([message, m])           
            return
        else:
            Config.RECORDING_TITLE=title
            await sync_to_db()
            await m.edit(f"Succesfully changed recording title to {title}")
            await delete_messages([message, m])
            return
    else:
        if not Config.HEROKU_APP:
            buttons = [[InlineKeyboardButton('Heroku API_KEY', url='https://dashboard.heroku.com/account/applications/authorizations/new'), InlineKeyboardButton('🗑 Close', callback_data='close'),]]
            await m.edit(
                text="No heroku app found, this command needs the following heroku vars to be set.\n\n1. <code>HEROKU_API_KEY</code>: Your heroku account api key.\n2. <code>HEROKU_APP_NAME</code>: Your heroku app name.", 
                reply_markup=InlineKeyboardMarkup(buttons)) 
            await delete_messages([message])
            return     
        config = Config.HEROKU_APP.config()
        if title == "False":
            if "RECORDING_TITLE" in config:
                await m.edit(f"Sucessfully removed custom recording title. Now restarting..")
                await delete_messages([message])
                del config["RECORDING_TITLE"]                
                config["RECORDING_TITLE"] = None
            else:
                await m.edit(f"Its already default title, nothing was changed")
                Config.RECORDING_TITLE=False
                await delete_messages([message, m])
        else:
            await m.edit(f"Succesfully changed recording title to {title}, Now restarting")
            await delete_messages([message])
            config["RECORDING_TITLE"] = title