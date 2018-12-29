import discord
from src.currencySystem import currencysystem

class InfoEmbed:
    def __init__(self, bot):
        self._bot = bot

    async def GenerateInfoEmbed(self, ctx):
        bot_latency = str(int(self._bot.latency * 100))
        bot_guildCount = str(len(self._bot.guilds))
        bot_userCount = str(len(self._bot.users))

        currency_system = currencysystem(self._bot)
        db_userCount = str(await currency_system.getUserCount)

        info_embed = discord.Embed(title="Info", color=0x9b59b6)
        info_embed.add_field(name="Anzahl von Servern", value=bot_guildCount + " 🖥️", inline=True)
        info_embed.add_field(name="Anzahl von Nutzern", value=bot_userCount + " 🤖", inline=True)
        info_embed.add_field(name="Nutzer in Datenbank", value=db_userCount)
        info_embed.add_field(name="WebSocket Latenz", value=bot_latency + " ms", inline=True)
        info_embed.add_field(name="Autor", value="<@231450290375622657>", inline=True)
        info_embed.add_field(name="Quellcode", value="https://github.com/nurlennart/Agara", inline=False)

        return info_embed
