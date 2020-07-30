# Utilities
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Imports
from discord.ext import commands
from discord import Guild, Role

# Loading config file...
with open("./config.json", "r", encoding="utf-8") as config:
    configFile = json.load(config)


class Roles(commands.Cog, name="Roles management"):
    def __init__(self, client):
        self.client = client

        # MySQL
        self.connectionStr = configFile["config"]["db"]

        # MySQL SQLAlchemy Engine Creation
        self.MySQLEngine = create_engine(
            self.connectionStr,
            pool_size=10,
            pool_recycle=3600,
            max_overflow=5,
            echo=True
        )

        # SQL Alchemy session
        self.sqlSession = sessionmaker(bind=self.MySQLEngine)
        self.session = self.sqlSession()

    
    @commands.command(name="Get channel roles", pass_context=True)
    async def role(self, ctx, command_='get', role: Role = None):
        roles = await Guild.fetch_roles(ctx.guild)
        print(roles)

def setup(client):
    client.add_cog(Roles(client))
