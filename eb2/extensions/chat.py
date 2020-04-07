from discord.ext import commands

class ChatControl(commands.Cog, name="Chat management commands"):
    def __init__(self, client):
        self.client = client
    
    @commands.command(pass_context = True)
    async def clear(self, ctx, amount = 10):
        if amount < 1:
            await ctx.send(f":x: The amount cannot be less than 1!")
            return
        try:
            amount = int(amount)
        except Exception:
            await ctx.send(f":x: {amount} is not a number! Try again!")
        deleted = await ctx.channel.purge(limit=amount)
        if len(deleted) < 1:
            await ctx.send(":x: Couldn't delete the messages")
            return
        messages = [f":white_check_mark: Deleted all **{amount}** messages!",
                    f":white_check_mark: Deleted **{amount}** message!"]
        if len(deleted) == 1:
            await ctx.send(messages[1])
            return

        await ctx.send(messages[0])
    
def setup(client):
    client.add_cog(ChatControl(client))
