import discord
from configparser import SafeConfigParser
import pymongo
import asyncio

# init config
parser = SafeConfigParser()
parser.read('config.ini')

class mongo:
    async def Connection():
        # init database connection
        mongo_client = pymongo.MongoClient("mongodb+srv://" + str(parser.get('mongodb', 'auth_string')) + "@cluster0-1fhvf.mongodb.net/agara?retryWrites=true")
        db = mongo_client['agara']
        return db
