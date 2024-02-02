# Copyright (C) @subinps
# Update By (C) @theSmartBisnu
# Channel : https://t.me/itsSmartDev


from pyrogram import Client
from config import Config
bot = Client(
    "VCPlayer",
    Config.API_ID,
    Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="plugins")
)