# Utilities
import json
from sqlalchemy import create_engine

# Imports
from discord.ext import commands
from discord import Guild

# Loading config file...
with open("./config.json", "r", encoding="utf-8") as config:
    configFile = json.load(config)

# MySQL
connectionStr = configFile["config"]["db"]

# MySQL Alchemy Engine Creation
MySQLEngine = create_engine(connectionStr, pool_size=10, pool_recycle=3600)

class Roles(commands.Cog, name="Roles management"):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name="Get channel roles", aliases=["roles.getall"], pass_context=True)
    async def roles(self, ctx):
        roles = await Guild.fetch_roles(ctx.guild)
        print(roles)

def setup(client):
    client.add_cog(Roles(client))
