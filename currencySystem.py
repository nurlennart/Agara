import discord
from discord.ext import commands
from configparser import SafeConfigParser
import asyncio
import pymongo
from database import mongo

class currencysystem:
    async def registerUser(ctx):
        userId = int(ctx.message.author.id)
        userName = str(ctx.message.author)
        guildId = int(ctx.message.guild.id)

        db = await mongo.Connection()
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

            currencysystem_add = discord.Embed(title="Punktesystem", color=0x9b59b6, description="Du wurdest zum Punktesystem hinzugefügt. Viel Spaß beim sammeln! 🤑")
            await ctx.send(embed=currencysystem_add)
        except Exception as err:
            print(str(err) + " while adding user to currencySystem. It probably already exists in database.")
            currencysystem_add_error = discord.Embed(title="Ups, da ist was schiefgelaufen", color=0xe74c3c, description="Entweder bist du bereits im Punktesystem, oder die Datenbank brennt mal wieder. Call 911.")
            await ctx.send(embed=currencysystem_add_error)

    async def unregisterUser(ctx):
        userId = int(ctx.message.author.id)
        guildId = int(ctx.message.guild.id)
        userName = str(ctx.message.author)

        db = await mongo.Connection()
        currencysystem = db.currencysystem
        try:
            result = currencysystem.delete_one( { "userid" :userId, "guildid" :guildId } )
            print("user " + userName + " removed from currencySystem")

            currencysystem_remove = discord.Embed(title="Punktesystem", color=0x9b59b6, description="Du wurdest aus dem Punktesystem entfernt.")
            await ctx.send(embed=currencysystem_remove)
        except Exception as err:
            print(str(err) + " while removing user from currencySystem.")
            currencysystem_remove_error = discord.Embed(title="Ups, da ist was schiefgelaufen", color=0xe74c3c, description="Entweder bist du noch gar nicht im Punktesystem, oder die Datenbank brennt mal wieder. Call 911.")
            await ctx.send(embed=currencysystem_remove_error)

    async def unregisterWholeGuild(guild):
        guildId = guild.id

        db = await mongo.Connection()
        currencysystem = db.currencysystem
        currencysystem.delete_many( { "guildid" :guildId })

    async def updateMessageCount(userId, guildId):
        db = await mongo.Connection()
        currencysystem = db.currencysystem

        currencysystem.update_one(
            {"userid": userId, "guildid" : guildId},
                {
                "$inc": {
                    "messagecount" : 1,
                    "balance" : 0.1
                }
            }
        )

    async def showBalance(ctx):
        userId = int(ctx.message.author.id)
        guildId = int(ctx.message.guild.id)
        userName = str(ctx.message.author.mention)

        db = await mongo.Connection()
        currencysystem = db.currencysystem
        try:
            balance = currencysystem.find_one({ "userid":userId, "guildid":guildId })

            currencysystem_balance = discord.Embed(title="Punktesystem", color=0x9b59b6)
            currencysystem_balance.add_field(name="Kontostand", value=userName + " besitzt aktuell **" + str(balance['balance']) + "** AgaCoins 💰", inline=True)
            await ctx.send(embed=currencysystem_balance)
        except Exception as err:
            currencysystem_balance_error = discord.Embed(title="Ups, da ist was schiefgelaufen", color=0xe74c3c, description="Entweder bist du noch gar nicht im Punktesystem, oder die Datenbank brennt mal wieder. Call 911.")
            await ctx.send(embed=currencysystem_balance_error)
