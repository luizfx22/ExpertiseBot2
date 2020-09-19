import json
import hashlib
import sqlite3
from pathlib import Path

# Imports
from discord.ext import commands

class CogMan(commands.Cog, name="ExpertiseBot core commands"):
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
            await ctx.message.delete()

            message = await ctx.send(":clock4: Reloading extensions!")
            # Reading all extensions added in config.json
            self.extensions = self.configFile["extensions"]
            for extension in self.extensions:
                try:
                    self.client.reload_extension(extension)
                    print(f" ~> Extension {extension} reloaded successfully!")

                except Exception as e:
                    print(f" ~> Cannot reload cog due to [{e}]")
                    await ctx.send(":x: Couldn't reload all extensions!")
            await message.delete()
            message = await ctx.send(":white_check_mark: All extensions reloaded successfully!")
            await message.delete(delay=2)

def setup(client):
    client.add_cog(CogMan(client))
