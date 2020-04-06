import json
import hashlib
import sqlite3
from pathlib import Path

# Imports
from discord.ext import commands

class CogMan(commands.Cog, name="Extension manager for ExpertiseBot"):
    def __init__(self, client):
        self.client = client
        self.loadedPlugins = []
        
        # Loading config file...
        with open("./config.json", "r", encoding="utf-8") as config:
            self.configFile = json.load(config)

        # Reading all extensions added in config.json
        self.extensions = self.configFile["extensions"]
        for extension in self.extensions:
            try:
                client.load_extension(extension)
                print(f" ~> Extension [{extension}] loaded with success!")
            except Exception as e:
                print(f" ~> Cannot load cog due to [{e}]")

    @commands.command(name="reload", pass_context=True)
    async def reload(self, ctx):
        async with ctx.typing():
            await ctx.send("Reloading extensions!")
            # Reading all extensions added in config.json
            self.extensions = self.configFile["extensions"]
            for extension in self.extensions:
                try:
                    self.client.reload_extension(extension)
                    print(f" ~> Extension {extension} reloaded successfully!")

                except Exception as e:
                    print(f" ~> Cannot reload cog due to [{e}]")
                    await ctx.send("Couldn't reload all extensions!")

            await ctx.send("All extensions reloaded successfully!")

def setup(client):
    client.add_cog(CogMan(client))
