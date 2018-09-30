import discord
import json, requests
from configparser import SafeConfigParser
import asyncio

parser = SafeConfigParser()
parser.read('config.ini')
class weatherEmbed:
    def __init__(self, ctx):
        self._ctx = ctx

    # get weather and send weather embed as response
    async def weatherGetter(self, City):
        WeatherApiKey = parser.get('weather', 'apikey')
        url = 'https://api.openweathermap.org/data/2.5/weather?q=' + City + '&appid=' + WeatherApiKey + '&units=metric&lang=de'

        resp = requests.get(url=url)
        data = resp.json()
        resp_code = data['cod']

        if resp_code == 200:
            # weather variables
            weather_description = data['weather'][0]['description']
            weather_temperature = data['main']['temp']
            weather_humidity = data['main']['humidity']
            weather_wind = data['wind']['speed']
            weather_icon = data['weather'][0]['icon']
            weather_icon_url = 'http://openweathermap.org/img/w/' + weather_icon + ".png"

            weather_embed = discord.Embed(title="Wetter für " + City, color=0x9b59b6)
            weather_embed.set_thumbnail(url=weather_icon_url)
            weather_embed.add_field(name="Aktuell", value=weather_description, inline=True)
            weather_embed.add_field(name="Aktuelle Temperatur", value=str(weather_temperature) + " °C", inline=True)
            weather_embed.add_field(name="Luftfeuchtigkeit", value=str(weather_humidity) + " %", inline=True)
            weather_embed.add_field(name="Wind", value=str(int(weather_wind) * 3.6) + " km/h", inline=True)

            await self._ctx.send(embed=weather_embed)

        else:
            weather_error_embed = discord.Embed(title="Ups", description="Der angegebene Ort existiert vermutlich nicht.", color=0xe74c3c)
            await self._ctx.send(embed=weather_error_embed)
