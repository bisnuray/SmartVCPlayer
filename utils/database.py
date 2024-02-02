# Copyright (C) @subinps
# Update By (C) @theSmartBisnu
# Channel : https://t.me/itsSmartDev

from .logger import LOGGER
import motor.motor_asyncio
from config import Config

class Database:    
    def __init__(self):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(Config.DATABASE_URI)
        self.db = self._client[Config.DATABASE_NAME]
        self.col = self.db.config
        self.playlist = self.db.playlist
    def new_config(self, name, value, dvalue):
        return dict(
            name = name,
            dvalue = dvalue,
            value = value,
        )   
    def add_config(self, name, value, dvalue=None):
        config = self.new_config(name, value, dvalue)
        self.col.insert_one(config)
    
    def new_song(self, id_, song):
        return dict(
            id = id_,
            song = song,
        )

    def add_to_playlist(self, id_, song):
        song_ = self.new_song(id_, song)
        self.playlist.insert_one(song_)
    
    
    async def is_saved(self, name):
        config = await self.col.find_one({'name':name})
        return True if config else False
     
    async def edit_config(self, name, value):
        await self.col.update_one({'name': name}, {'$set': {'value': value}})
    
    async def edit_default(self, name, dvalue):
        await self.col.update_one({'name': name}, {'$set': {'dvalue': dvalue}})
    
    async def get_default(self, name):
        config = await self.col.find_one({'name':name})
        return config.get('dvalue')

    async def get_config(self, name):
        config = await self.col.find_one({'name':name})
        return config.get('value')

    async def del_config(self, name):
        await self.col.delete_one({'name':name})
        return
    
    async def is_in_playlist(self, id_):
        song = await self.playlist.find_one({'id':id_})
        return True if song else False
     

    async def get_song(self, id_):
        song_ = await self.playlist.find_one({'id':id_})
        return song_.get('song')

    async def del_song(self, id_):
        await self.playlist.delete_one({'id':id_})
        return

    async def clear_playlist(self):
        await self.playlist.drop()
        return
    
    async def get_playlist(self):
        k = self.playlist.find({})
        l=[]
        async for song in k:
            song_ = {int(k):v for k,v in song['song'].items()}
            l.append(song_)
        return l

db=Database()