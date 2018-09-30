import discord
import json, requests
from configparser import SafeConfigParser
import asyncio

parser = SafeConfigParser()
parser.read('config.ini')
class gifHandler:
    def __init__(self, bot):
        self._bot = bot

    # get gif from giphy api and respond with an gif that fits the given keyword
    async def getGif(self, ctx, query):
        GiphyApiKey = parser.get('giphy', 'apikey')
        url = 'https://api.giphy.com/v1/gifs/random?api_key=' + GiphyApiKey + '&tag=' + query + '&rating=G'

        resp = requests.get(url=url)
        data = resp.json()
        resp_code = data['meta']['status']

        if resp_code == 200:
            gif_url = data['data']['images']['original']['url']

            gif_embed = discord.Embed(title=query + " GIF", color=0x9b59b6)
            gif_embed.set_footer(text="powered by GIPHY")
            gif_embed.set_image(url=gif_url)
            await ctx.send(embed=gif_embed)

            return True
        else:
            gif_error_embed = discord.Embed(title="Ups", description="Da ist was schiefgelaufen.", color=0xe74c3c)
            await ctx.send(embed=gif_error_embed)
            return False
