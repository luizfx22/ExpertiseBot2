from discord.ext import commands

class Cogs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="reload", pass_context=True)
    @commands.is_owner
    async def reload(self, ctx):
        ctx.send("Reloading...")
        



def setup(client):
    client.add_cog(Cogs(client))
