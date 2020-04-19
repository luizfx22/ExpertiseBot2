from discord import Embed, Colour, Guild
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
        async with ctx.typing():
            deleted = await ctx.channel.purge(limit=amount)
            if len(deleted) < 1:
                await ctx.send(":x: Couldn't delete the messages")
                return

            messages = [f":white_check_mark: Deleted all **{len(deleted)}** messages!",
                        f":white_check_mark: Deleted **{len(deleted)}** message!"]
            if len(deleted) == 1:
                message = await ctx.send(messages[1])
                await message.delete(delay=5)
                return

            message = await ctx.send(messages[0])
            await message.delete(delay=5)

    @commands.command(pass_context = True)
    async def alert(self, ctx, title="Titulo", description="Descrição"):
        await ctx.message.delete()

        await ctx.send("Hey @everyone!")

        user = Guild.get_member(ctx.message.author.guild, user_id=ctx.message.author.id)

        embed = Embed()
        embed.title = title
        embed.description = description
        embed.colour = Colour.gold()
        embed.set_author(name=ctx.message.author.name, icon_url=user.avatar_url)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(ChatControl(client))
