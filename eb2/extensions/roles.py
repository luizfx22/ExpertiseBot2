# Imports
from discord.ext import commands

class Roles(commands.Cog, name="Roles management"):
    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(Roles(client))
