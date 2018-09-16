import discord
from discord.ext import commands
import json, requests
from configparser import SafeConfigParser
import asyncio
from commands.commandWeather import weatherEmbed
from commands.commandInfo import InfoEmbed
from commands.startPoll import Poll
from database import mongo
from currencySystem import currencysystem

# init bot
bot = commands.Bot(command_prefix='!')
bot.remove_command("help")
# init config
parser = SafeConfigParser()
parser.read('config.ini')

infoEmbed = InfoEmbed(bot)

poll = Poll(bot)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('---- Time to take over the world. lawl. ----')

    db = await mongo.Connection()
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
    game = discord.Game(str(len(bot.guilds)) + " Server" + " | !hilfe")
    await bot.change_presence(activity=game)

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    userId = message.author.id
    guildId = message.guild.id

    if message.content.startswith('!'):
        return
    else:
        await currencysystem.updateMessageCount(userId, guildId)

@bot.event
async def on_guild_join(guild):
    db = await mongo.Connection()
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

@bot.event
async def on_guild_remove(guild):
    db = await mongo.Connection()
    guilds = db.guilds
    result = guilds.delete_one( { "guildId" :guild.id } )
    print(result)

    await updateGame()

    await currencysystem.unregisterWholeGuild(guild)

@bot.command(aliases=["wetter"])
async def weather(ctx, City):
    await weatherEmbed.weatherGetter(ctx, City)
    print(str(ctx.message.author) + " requested the weather of " + City)

@bot.command()
async def info(ctx):
    await ctx.send(embed=await infoEmbed.GenerateInfoEmbed(ctx))

@bot.command()
async def startpoll(ctx, question, seconds):
    print(str(ctx.message.author) + " started a new poll. It will end in " + seconds + " seconds")

    poll_message = await ctx.send(embed=await poll.GeneratePollEmbed(ctx, question, seconds))
    upvote = await poll_message.add_reaction("➕")
    downvote = await poll_message.add_reaction("➖")
    await asyncio.sleep(int(seconds))

    poll_message_ = await ctx.get_message(poll_message.id)

    reactions = {react.emoji: react.count for react in poll_message_.reactions}

    upvotes = reactions["➕"]
    downvotes = reactions["➖"]

    await poll_message.delete()

    await ctx.send(embed=await poll.GeneratePollResultEmbed(ctx, question, upvotes, downvotes))

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

@bot.command()
async def register(ctx):
    await currencysystem.registerUser(ctx)

@bot.command()
async def unregister(ctx):
    await currencysystem.unregisterUser(ctx)

@bot.command(aliases=["kontostand", "agacoins"])
async def balance(ctx):
    await currencysystem.showBalance(ctx)

@bot.command(alias=["hilfe"])
async def help(ctx):
    help_embed = discord.Embed(title="Hier werden Sie geholfen!", color=0x9b59b6)
    help_embed.add_field(name="__Punktesystem__\n", value="Das Punktesystem weist dir (wenn du registriert bist), für jede geschriebene Nachricht 0.1 Punkte zu. In Zukunft wird es möglich sein, mit diesen Punkten exklusive Befehle zu nutzen, sodass sich das Registrieren im Punktesystem auch lohnt. 🙂", inline=True)
    help_embed.add_field(name="!register", value="Fügt dich zum Punktesystem hinzu")
    help_embed.add_field(name="!unregister", value="Löscht dich aus dem Punktesystem")
    help_embed.add_field(name="!balance (!kontostand, !agacoins)", value="Zeigt dir deinen aktuellen Kontostand")
    help_embed.add_field(name="__Allgemeine Befehle__", value="Agara hat noch mehr als nur das Punktesystem drauf, ich schwöre!", inline=True)
    help_embed.add_field(name="!help (!hilfe)", value="Ähm ja, da bist du gerade.")
    help_embed.add_field(name="!weather (!wetter) 'ort'", value="Erklärt sich von selbst, huh? Wetter und so.")
    help_embed.add_field(name="!info", value="Zeigt ein paar Statistiken von Agara")
    help_embed.add_field(name="!hug @nutzername", value="Mal ein bisschen Liebe verschenken und die tolle Emoji Animation bewundern, die ich mit viel Liebe gebaut habe.")
    help_embed.add_field(name="!startpoll 'umfrage' <sekunden>", value="Damit könnt ihr kleine Umfragen starten. Wird vermutlich eines der AgaCoins Features. Man kann aktuell noch mit Ja und Nein gleichzeitig stimmen, aber das bekomm' ich bestimmt auch noch in den Griff.")

    await ctx.send(embed=help_embed)

# run the bot
bot.run(parser.get('agara', 'token'))
