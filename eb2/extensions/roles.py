# Imports
from discord.ext import commands
from discord import Guild

class Roles(commands.Cog, name="Roles management"):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name="Get channel roles", aliases=["roles.getall"], pass_context=True)
    async def roles(self, ctx):
        roles = await Guild.fetch_roles(ctx.guild)
        print(roles)

def setup(client):
    client.add_cog(Roles(client))
