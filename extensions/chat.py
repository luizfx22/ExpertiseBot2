import discord
from discord.ext import commands

class Chat_Control(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(pass_context = True)
    async def delete(self, ctx, msg = 10):
        await ctx.send("Hai")


def setup(client):
    client.add_cog(Chat_Control(client))