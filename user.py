# Copyright (C) @subinps
# Update By (C) @theSmartBisnu
# Channel : https://t.me/itsSmartDev


from pytgcalls import PyTgCalls
from pyrogram import Client
from config import Config
from utils import LOGGER

USER = Client("userSession", Config.API_ID, Config.API_HASH, session_string=Config.SESSION, plugins=dict(root="userplugins"))
     
group_call = PyTgCalls(USER, cache_duration=180)
