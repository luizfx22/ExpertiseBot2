import json
import hashlib
import sqlite3

# Imports
from discord.ext import commands

class CogMan(commands.Cog, name="Extension manager for ExpertiseBot"):
    def __init__(self, client):
        self.client = client
        
        # Create or load SQLite3 database and cursor
        try:
            connection = sqlite3.connect("./public/plugins.db")
        except Exception:
            with open('./public/plugins.db', 'w') as dbFile:
                dbFile.close()
            connection = sqlite3.connect("./public/plugins.db")
        
        cursor = connection.cursor()

        # Creating table if not exists
        query = """
            CREATE TABLE IF NOT EXISTS plugins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                PluginName TEXT NOT NULL,
                PluginMain TEXT NOT NULL,
                PluginDirectory TEXT NOT NULL
            )
        """
        cursor.execute(query)
        connection.commit()

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
        
        print(" -> Indexing plugins...")

        # Start indexing all installed plugins
        plugins = cursor.execute("SELECT * FROM plugins")
        if len(plugins) == 0:
            print(" - Found nothing! Skipping...")

        for plugin in plugins:
            print(plugin)

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

    @commands.command(name="install", pass_context=True)
    async def install(self, ctx, options, name):
        pass
    
    @commands.command(name="ghash", pass_context=True)
    async def ghash(self, ctx, name):
        fname = hashlib.sha256(name.encode('utf-8')).hexdigest()
        await ctx.send(f"Hi! To make your extension a valid extension, please,\nplace this value in the hash section inside your `meta.json`")
        await ctx.send(f"```{fname}```")

def setup(client):
    client.add_cog(CogMan(client))
