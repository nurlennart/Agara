import discord
from discord.ext import commands
import json, requests
from configparser import SafeConfigParser
import asyncio
import pymongo
import datetime
from commands.commandWeather import weatherEmbed
from commands.commandInfo import InfoEmbed
from commands.commandGif import gifHandler
from commands.commandStartPoll import Poll
from src.currencySystem import currencysystem

# init bot
bot = commands.Bot(command_prefix='aga!')
bot.remove_command("help")
# init config
parser = SafeConfigParser()
parser.read('config.ini')

infoEmbed = InfoEmbed(bot)
poll = Poll(bot)
currency_system = currencysystem(bot)

mongo_client = pymongo.MongoClient("mongodb+srv://" + str(parser.get('mongodb', 'auth_string')) + "@cluster0-1fhvf.mongodb.net/agara?retryWrites=true")

# print that the bot is ready and all guilds to the database
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('---- Time to take over the world. lawl. ----')

    db = mongo_client['agara']
    guilds = db.guilds
    guilds.ensure_index('guildId', unique=True)
    # add all guilds to database on startup
    for guild in bot.guilds:
        guildId = guild.id
        guildName = guild.name
        guildToInsert = {
            'guildName' : guildName,
            'guildId' : guildId
        }
        try:
            result = guilds.insert_one(guildToInsert)
            print(result)
        except Exception as err:
            print(str(err) + " while adding guild. It probably already exists in database.")

    await updateGame()

async def updateGame():
    # change game
    game = discord.Game(str(len(bot.guilds)) + " Server" + " | aga!hilfe")
    await bot.change_presence(activity=game)

# process received messages as command or message for the currencysystem
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    userId = message.author.id
    guildId = message.guild.id

    if message.content.startswith(('!', '?', '~', 'aga!')):
        return
    else:
        if(message.author.bot != True):
            checkForUser = await currency_system.userExists(userId, guildId)
            if(checkForUser != None):
                await currency_system.updateMessageCount(userId, guildId)
                currentTime = str(now.strftime("%H:%M"))
                print(currentTime + " received message, +0,1 agacoins for someone.")
            else:
                await currency_system.registerUser(message)
                await currency_system.updateMessageCount(userId, guildId)
        else:
            return

# add guild to guilds database on join
@bot.event
async def on_guild_join(guild):
    db = mongo_client['agara']
    guilds = db.guilds
    guilds.ensure_index('guildId', unique=True)

    guildToInsert = {
        'guildName' : guild.name,
        'guildId' : guild.id
    }
    try:
        result = guilds.insert_one(guildToInsert)
        print("guild added to database. result:" + str(result))
    except Exception as err:
        print(str(err) + " while adding joined guild. It probably already exists in database.")

    await updateGame()

# delete guild from guilds database and unregister every from this guild in currencysystem on guild leave
@bot.event
async def on_guild_remove(guild):
    db = mongo_client['agara']
    guilds = db.guilds
    result = guilds.delete_one( { "guildId" :guild.id } )
    print(result)

    await updateGame()

    await currency_system.unregisterWholeGuild(guild)

# remove member from database on remove/leave
@bot.event
async def on_member_remove(member):
    userId = member.id
    guildId = member.guild.id

    if await currency_system.userExists(userId, guildId) != None:
        await currency_system.unregisterUser(member)
    else:
        return

# leaderboard command
@bot.command(aliases=["bestenliste"])
async def leaderboard(ctx):
    await currency_system.leaderboard(ctx)
    print(str(ctx.message.author) + " requested the leaderboard of guild " + str(ctx.message.guild.id))

# balance command
@bot.command(aliases=["kontostand", "agacoins"])
async def balance(ctx):
    await currency_system.showBalance(ctx)
    print(str(ctx.message.author) + " requested his balance")

# weather command
@bot.command(aliases=["wetter"])
async def weather(ctx, City):
    weather = weatherEmbed(ctx)
    await weather.weatherGetter(City)
    print(str(ctx.message.author) + " requested the weather of " + City)

# info/stats command
@bot.command()
async def info(ctx):
    await ctx.send(embed=await infoEmbed.GenerateInfoEmbed(ctx))

# poll command
@bot.command()
async def startpoll(ctx, question, seconds):
    print(str(ctx.message.author) + " started a new poll. It will end in " + seconds + " seconds")

    poll_message = await ctx.send(embed=await poll.GeneratePollEmbed(ctx, question, seconds))
    await poll_message.add_reaction("➕")
    await poll_message.add_reaction("➖")
    await asyncio.sleep(int(seconds))

    poll_message_ = await ctx.get_message(poll_message.id)

    reactions = {react.emoji: react.count for react in poll_message_.reactions}

    upvotes = reactions["➕"]
    downvotes = reactions["➖"]

    await poll_message.delete()

    await ctx.send(embed=await poll.GeneratePollResultEmbed(ctx, question, upvotes, downvotes))

# hug command
@bot.command()
async def hug(ctx, userToHug):
    hugColor = 0x9b59b6

    embed1 = discord.Embed(title=str(ctx.message.author) + " hugs ", color=hugColor, description="🤖----🤖 " + userToHug)
    embed2 = discord.Embed(title=str(ctx.message.author) + " hugs ", color=hugColor, description="🤖---🤖 " + userToHug)
    embed3 = discord.Embed(title=str(ctx.message.author) + " hugs ", color=hugColor, description="🤖--🤖 " + userToHug)
    embed4 = discord.Embed(title=str(ctx.message.author) + " hugs ", color=hugColor, description="🤖-🤖 " + userToHug)
    embed5 = discord.Embed(title=str(ctx.message.author) + " hugs ", color=hugColor, description="🤖💚🤖 " + userToHug)
    embed6 = discord.Embed(title=str(ctx.message.author) + " hugs ", color=hugColor, description="🤖💫💜💫🤖 " + userToHug)
    embed7 = discord.Embed(title=str(ctx.message.author) + " hugs ", color=hugColor, description="🤖💗🤖 " + userToHug)

    message = await ctx.send(embed=embed1)

    await asyncio.sleep(0.5)
    await message.edit(embed=embed2)
    await asyncio.sleep(0.5)
    await message.edit(embed=embed3)
    await asyncio.sleep(0.5)
    await message.edit(embed=embed4)
    await asyncio.sleep(0.5)
    await message.edit(embed=embed5)
    await asyncio.sleep(0.5)
    await message.edit(embed=embed6)
    await asyncio.sleep(2)
    await message.edit(embed=embed7)

# gif command
@bot.command()
async def gif(ctx, query):
    print(str(ctx.message.author) + " requested a gif with the query " + str(query))

    userId = int(ctx.author.id)
    guildId = int(ctx.guild.id)
    gif = gifHandler(bot)

    db = mongo_client['agara']
    currencysystem = db.currencysystem
    getFromDb = currencysystem.find_one({ "userid":userId, "guildid":guildId })

    if getFromDb != None:
        userBalance = getFromDb['balance']
        if int(userBalance) >= 1:
            sendGif = await gif.getGif(ctx, query)
            if sendGif == True:
                currencysystem.update_one(
                    {"userid": userId, "guildid": guildId},
                        {
                        "$inc": {
                            "balance" : -1
                        }
                    }
                )
            else:
                return
        else:
            balance_not_sufficient = discord.Embed(title="AgaCoins nicht ausreichend", description="Das kannst du dir mit deinen **" + str(userBalance) + "** AgaCoins noch nicht leisten. !gif kostet **1** AgaCoin. 😭", color=0x9b59b6)
            await ctx.send(embed=balance_not_sufficient)
    else:
        user_not_in_currencysystem = discord.Embed(title="Das wird nichts.", description="Das ist ein AgaCoin Feature. Um dieses zu nutzen, musst du dich im Punktesystem registrieren (**!register**) und Punkte sammeln. Tu es, es lohnt sich! 🤫", color=0x9b59b6)
        await ctx.send(embed=user_not_in_currencysystem)

# !help
@bot.command(aliases=["hilfe"])
async def help(ctx):
    help_embed = discord.Embed(title="Hier werden Sie geholfen!", color=0x9b59b6)
    help_embed.add_field(name="__Punktesystem__\n", value="Das Punktesystem weist dir für jede geschriebene Nachricht 0.1 Punkte zu. In Zukunft wird es möglich sein, mit diesen Punkten exklusive Befehle zu nutzen. 🙂", inline=True)
    help_embed.add_field(name="aga!balance (aga!kontostand, aga!agacoins)", value="Zeigt dir deinen aktuellen Kontostand")
    help_embed.add_field(name="aga!leaderboard", value="Zeigt dir die Nutzer mit den meisten Nachrichten/AgaCoins an")
    help_embed.add_field(name="__Allgemeine Befehle__", value="Agara hat noch mehr als nur das Punktesystem drauf, ich schwöre!", inline=True)
    help_embed.add_field(name="aga!help (aga!hilfe)", value="Ähm ja, da bist du gerade.")
    help_embed.add_field(name="aga!weather (aga!wetter) 'ort'", value="Erklärt sich von selbst, huh? Wetter und so.")
    help_embed.add_field(name="aga!hug @nutzername", value="Mal ein bisschen Liebe verschenken und die tolle Emoji Animation bewundern, die ich mit viel Liebe gebaut habe.")
    help_embed.add_field(name="aga!startpoll 'umfrage' <sekunden>", value="Damit könnt ihr kleine Umfragen starten. Wird vermutlich eines der AgaCoins Features. Man kann aktuell noch mit Ja und Nein gleichzeitig stimmen, aber das bekomm' ich bestimmt auch noch in den Griff.")
    help_embed.add_field(name="aga!info", value="Zeigt ein paar Statistiken von Agara.")
    # agacoins commands from here
    help_embed.add_field(name="__AgaCoins Befehle __", value="Hier sind die Befehle, für die ihr eure AgaCoins einsetzen könnt. Ich weiß, der Name der Währung ist unfassbar kreativ.", inline=True)
    help_embed.add_field(name="aga!gif 'suchbegriff' | **kostet 1 AgaCoin**", value="Bring deine Gefühle mit 'nem GIF zum Ausdruck. Cat GIFs forever.")
    await ctx.send(embed=help_embed)

# run the bot
bot.run(parser.get('agara', 'token'))
