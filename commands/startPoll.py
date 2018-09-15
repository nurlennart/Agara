import discord

class Poll:
    def __init__(self, bot):
        self._bot = bot

    async def GeneratePollEmbed(self, ctx, question, seconds):
        info_embed = discord.Embed(title="Poll [" + seconds + " Sekunden]", color=0xeee657)
        info_embed.add_field(name="Frage", value=question, inline=True)

        return info_embed

    async def GeneratePollResultEmbed(self, ctx, question, upvotes, downvotes):
        result_embed = discord.Embed(title="Poll Ergebnisse", color=0xeee657)
        result_embed.add_field(name="Frage", value=question, inline=True)
        result_embed.add_field(name="➕", value=int(upvotes) - 1)
        result_embed.add_field(name="➖", value=int(downvotes) -1)

        return result_embed
        #await ctx.send(embed=info_embed)
