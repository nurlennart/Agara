import discord
from discord.ext import commands
import json, requests
from configparser import SafeConfigParser
import asyncio

bot = commands.Bot(command_prefix='!')

parser = SafeConfigParser()
parser.read('config.ini')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    # change game
    game = discord.Game("Development.")
    await bot.change_presence(activity=game)


@bot.command()
async def weather(ctx, City):
    WeatherApiKey = parser.get('weather', 'apikey')
    url = 'https://api.openweathermap.org/data/2.5/weather?q=' + City + '&appid=' + WeatherApiKey + '&units=metric&lang=de'

    resp = requests.get(url=url)
    data = resp.json()

    # weather variables
    weather_description = data['weather'][0]['description']
    weather_temperature = data['main']['temp']
    weather_humidity = data['main']['humidity']
    weather_wind = data['wind']['speed']
    weather_icon = data['weather'][0]['icon']

    weather_icon_url = 'http://openweathermap.org/img/w/' + weather_icon + ".png"

    weather_embed = discord.Embed(title="Wetter für " + City, color=0xeee657)
    weather_embed.set_thumbnail(url=weather_icon_url)
    weather_embed.add_field(name="Aktuell", value=weather_description, inline=True)
    weather_embed.add_field(name="Aktuelle Temperatur", value=str(weather_temperature) + " °C", inline=True)
    weather_embed.add_field(name="Luftfeuchtigkeit", value=str(weather_humidity) + " %", inline=True)
    weather_embed.add_field(name="Wind", value=str(int(weather_wind) * 3.6) + " km/h", inline=True)

    await ctx.send(embed=weather_embed)

bot.run(parser.get('agara', 'token'))
