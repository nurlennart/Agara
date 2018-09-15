import discord
from discord.ext import commands
import json, requests
from configparser import SafeConfigParser
import asyncio
from commands.commandWeather import weatherEmbed
from commands.commandInfo import InfoEmbed
from commands.startPoll import Poll

bot = commands.Bot(command_prefix='!')

infoEmbed = InfoEmbed(bot)

poll = Poll(bot)


parser = SafeConfigParser()
parser.read('config.ini')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    # change game
    game = discord.Game(str(len(bot.guilds)) + " Server")
    await bot.change_presence(activity=game)

@bot.command()
async def weather(ctx, City):
    await weatherEmbed.weatherGetter(ctx, City)
    print(str(ctx.message.author) + " requested the weather of " + City)

@bot.command()
async def info(ctx):
    #await InfoEmbed.GenerateInfoEmbed(ctx)
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
    hugColor = 0xeee657

    embed1 = discord.Embed(title=str(ctx.message.author) + " hugs " + str(userToHug), color=hugColor, description="🤖----🤖")

    embed2 = discord.Embed(title=str(ctx.message.author) + " hugs " + str(userToHug), color=hugColor, description="🤖---🤖")

    embed3 = discord.Embed(title=str(ctx.message.author) + " hugs " + str(userToHug), color=hugColor, description="🤖--🤖")

    embed4 = discord.Embed(title=str(ctx.message.author) + " hugs " + str(userToHug), color=hugColor, description="🤖-🤖")

    embed5 = discord.Embed(title=str(ctx.message.author) + " hugs " + str(userToHug), color=hugColor, description="🤖💚🤖")

    embed6 = discord.Embed(title=str(ctx.message.author) + " hugs " + str(userToHug), color=hugColor, description="🤖💫💜💫🤖")

    embed7 = discord.Embed(title=str(ctx.message.author) + " hugs " + str(userToHug), color=hugColor, description="🤖💗🤖")

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


# run the bot
bot.run(parser.get('agara', 'token'))
