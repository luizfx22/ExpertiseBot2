
import mysql.connector
from mysql.connector import errorcode
from discord import Embed, Colour, Guild
from discord.ext import commands
import re
import json
import random

class ChatControl(commands.Cog, name="Chat management commands"):
    def __init__(self, client):
        self.client = client
        
        # Loading config file...
        with open("./config.json", "r", encoding="utf-8") as config:
            configFile = json.load(config)

        print(f' >> Connecting to database with user {configFile["db-settings"]["user"]}!')

        try:
            self.connection = mysql.connector.connect(
                host=f'{configFile["db-settings"]["address"]}',
                user=f'{configFile["db-settings"]["user"]}',
                password=f'{configFile["db-settings"]["password"]}',
                database=f'{configFile["db-settings"]["database"]}'
            )

            print(" >> Database connection made!")

        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_BAD_DB_ERROR:
                print(" >> Database doesn't exist")
            elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print(" >> User name or password is wrong")
            else:
                print(error)
                raise Exception(error)
        
        self.cursor = self.connection.cursor()
    
    async def setup_backup(self, ctx):
        message = ctx.message
        guild = ctx.guild

        guild_id = guild.id

        sql = """INSERT IGNORE INTO sec_guilds (`id`, `name`) VALUES (%s, %s);"""
        
        embed = Embed(title="ExpertiseBot Channel Backup Utility", description="Using ExpertiseBot to create a backup of every message from any text channel available in guild.")
        embed.color = 0x5CA7AD
        embed.add_field(name="How to:", value="To create a backup you must set the channels to be watched and backup every message!")
        
        guild_text_channels = get

        await ctx.send(embed=embed)

        self.cursor.execute(sql, (guild.id, guild.name))

        self.connection.commit()

        await ctx.send(message.id)
        

        return True
    
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
    
    @commands.command(pass_context=True)
    async def backup(self, ctx, command):
        commands = {
            "setup": await self.setup_backup(ctx)
        }

        return commands[command]

def setup(client):
    client.add_cog(ChatControl(client))
