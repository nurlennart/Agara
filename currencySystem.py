import discord
from discord.ext import commands
from configparser import SafeConfigParser
import asyncio
import pymongo

parser = SafeConfigParser()
parser.read('config.ini')

mongo_client = pymongo.MongoClient("mongodb+srv://" + str(parser.get('mongodb', 'auth_string')) + "@cluster0-1fhvf.mongodb.net/agara?retryWrites=true")

class currencysystem:
    async def registerUser(message):
        userId = int(message.author.id)
        userName = str(message.author)
        guildId = int(message.guild.id)

        db = mongo_client['agara']
        currencysystem = db.currencysystem
        currencysystem.ensure_index([("guildid" , pymongo.DESCENDING),("userid", pymongo.ASCENDING)], unique=True)

        userRegistrationInfo = {
            'username' : userName,
            'userid' : userId,
            'guildid' : guildId,
            'balance' : 0,
            'messagecount' : 0
        }
        try:
            result = currencysystem.insert_one(userRegistrationInfo)
            print("user " + userName + " added to currencySystem")

            #currencysystem_add = discord.Embed(title="Punktesystem", color=0x9b59b6, description="Du wurdest zum Punktesystem hinzugefügt. Viel Spaß beim sammeln! 🤑")
            #await ctx.send(embed=currencysystem_add)
        except Exception as err:
            print(str(err) + " while adding user to currencySystem. It probably already exists in database.")
            currencysystem_add_error = discord.Embed(title="Ups, da ist was schiefgelaufen", color=0xe74c3c, description="Entweder bist du bereits im Punktesystem, oder die Datenbank brennt mal wieder. Call 911.")
            await message.channel.send(embed=currencysystem_add_error)

    async def unregisterUser(member):
        userId = int(member.id)
        guildId = int(member.guild.id)
        userName = str(member.display_name)

        db = mongo_client['agara']
        currencysystem = db.currencysystem
        try:
            result = currencysystem.delete_one( { "userid" :userId, "guildid" :guildId } )
            print("user " + userName + " removed from currencySystem")
        except Exception as err:
            print(str(err) + " while removing user from currencySystem.")

    async def unregisterWholeGuild(guild):
        guildId = guild.id

        db = mongo_client['agara']
        currencysystem = db.currencysystem
        currencysystem.delete_many( { "guildid" :guildId })

    async def updateMessageCount(userId, guildId):
        db = mongo_client['agara']
        currencysystem = db.currencysystem

        currencysystem.update_one(
            {"userid": userId, "guildid": guildId},
                {
                "$inc": {
                    "messagecount" : 1,
                    "balance" : 0.1
                }
            }
        )

    async def userExists(userId, guildId):
        db = mongo_client['agara']
        currencysystem = db.currencysystem

        check = currencysystem.find_one({ "userid":userId, "guildid":guildId })
        return(check)

    async def showBalance(ctx):
        userId = int(ctx.message.author.id)
        guildId = int(ctx.message.guild.id)
        userName = str(ctx.message.author.mention)

        db = mongo_client['agara']
        currencysystem = db.currencysystem
        try:
            balance = currencysystem.find_one({ "userid":userId, "guildid":guildId })

            currencysystem_balance = discord.Embed(title="Punktesystem", color=0x9b59b6)
            currencysystem_balance.add_field(name="Kontostand", value=userName + " besitzt aktuell **" + str(round(balance['balance'], 2)) + "** AgaCoins 💰", inline=True)
            await ctx.send(embed=currencysystem_balance)
        except Exception as err:
            currencysystem_balance_error = discord.Embed(title="Ups, da ist was schiefgelaufen", color=0xe74c3c, description="Entweder bist du noch gar nicht im Punktesystem, oder die Datenbank brennt mal wieder. Call 911.")
            await ctx.send(embed=currencysystem_balance_error)

    async def leaderboard(ctx, bot):
        db = mongo_client['agara']
        currencysystem = db.currencysystem

        usercount = 0
        guildId = ctx.guild.id
        find_guild = currencysystem.find_one({ "guildid" : guildId })

        if find_guild != None:
            five_highest = currencysystem.find({ "guildid" : guildId }, limit = 5).sort('messagecount', -1)

            currencysystem_leaderboard = discord.Embed(title="Leaderboard", color=0x9b59b6)
            count = 1
            inline_state = False
            for document in five_highest:
                user = discord.Client.get_user(bot, id=document['userid'])
                currencysystem_leaderboard.add_field(name=str(count) + ". " + str(user), value="**" + str(document['messagecount']) + "** Nachrichten | **" + str(round(document['balance'], 2)) + "** AgaCoins", inline=inline_state)
                count += 1
                if inline_state == False:
                    inline_state = True
                else:
                    inline_state = False
            await ctx.send(embed=currencysystem_leaderboard)
        else:
            currencysystem_leaderboard_error = discord.Embed(title="Server nicht in Datenbank", color=0xe74c3c, description="Kein Nutzer aus diesem Server befindet sich in der Datenbank. Nutzer werden nach ihrer ersten Nachricht eingetragen.")
            await ctx.send(embed=currencysystem_leaderboard_error)
