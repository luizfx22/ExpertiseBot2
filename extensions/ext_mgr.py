import json
import time
import hashlib

# Imports
import discord
from discord.ext import commands

class CogMan(commands.Cog, name="Extension manager for ExpertiseBot"):
    def __init__(self, client):
        self.client = client
        
        # Loading config file...
        with open("./config.json", "r", encoding="utf-8") as config:
            self.j = json.load(config)

        # Reading all extensions added in config.json
        self.extensions = self.j["extensions"]
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
            self.extensions = self.j["extensions"]
            for extension in self.extensions:
                try:
                    self.client.reload_extension(extension)
                    print(f" ~> Extension {extension} reloaded successfully!")

                except Exception as e:
                    print(f" ~> Cannot reload cog due to [{e}]")
                    await ctx.send("Couldn't reload all extensions!")

            await ctx.send("All extensions reloaded successfully!")

    @commands.command(name="install", pass_context=True)
    async def install(self, ctx, url):
        await ctx.send(f"Instalar {url}")
    
    @commands.command(name="ghash", pass_context=True)
    async def ghash(self, ctx, name):
        fname = hashlib.sha256(name.encode('utf-8')).hexdigest()
        await ctx.send(f"Hi! To make your extension a valid extension, please,\nplace this value in the hash section inside your `meta.json`")
        await ctx.send(f"```{fname}```")

def setup(client):
    client.add_cog(CogMan(client))
