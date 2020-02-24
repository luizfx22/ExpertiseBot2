import json

# Imports
from discord.ext import commands

class Cogs(commands.Cog):
    def __init__(self, client):
        self.client = client
        
        # Loading config file...
        with open("./config.json", "r", encoding="utf-8") as config:
            j = json.load(config)
        
        # Reading all extensions added in config.json
        extensions = j["extensions"]
        for extension in extensions:
            try:
                client.load_extension(extension)
                print(f" ~> Extension [{extension}] loaded with success!")
            except Exception as e:
                print(f" ~> Cannot load cog due to [{e}]")

    @commands.command(name="reload", pass_context=True)
    @commands.is_owner
    async def reload(self, ctx):
        ctx.send("Reloading...")


def setup(client):
    client.add_cog(Cogs(client))
