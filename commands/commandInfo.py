import discord

class InfoEmbed:
    def __init__(self, bot):
        self._bot = bot

    async def GenerateInfoEmbed(self, ctx):
        bot_latency = str(int(self._bot.latency * 100))
        bot_guildCount = str(len(self._bot.guilds))

        info_embed = discord.Embed(title="Info", color=0xeee657)
        info_embed.add_field(name="WebSocket Latenz", value=bot_latency + " ms", inline=True)
        info_embed.add_field(name="Anzahl von Servern", value=bot_guildCount, inline=True)
        info_embed.add_field(name="Autor", value="<@231450290375622657>", inline=True)
        info_embed.add_field(name="Uptime", value=str(minutes) + " Minuten", inline=True)
        info_embed.add_field(name="Quellcode", value="https://github.com/nurlennart/Agara_Python", inline=False)

        return info_embed

    async def uptimeCounter(self, bot):
        await bot.wait_until_ready()
        print("started uptimeCounter")
        global minutes
        minutes = 0
        while not bot.is_closed:
            await asyncio.sleep(60)
            minutes += 1
