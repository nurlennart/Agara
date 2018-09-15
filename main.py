import discord
from discord.ext import commands
import json, requests
from configparser import SafeConfigParser
import asyncio
from commands.commandWeather import weatherEmbed
from commands.commandInfo import InfoEmbed

bot = commands.Bot(command_prefix='!')

infoEmbed = InfoEmbed(bot)

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

@bot.command()
async def info(ctx):
    #await InfoEmbed.GenerateInfoEmbed(ctx)
    await ctx.send(embed=await infoEmbed.GenerateInfoEmbed(ctx))

# run the bot
bot.run(parser.get('agara', 'token'))
