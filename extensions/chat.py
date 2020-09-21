
import mysql.connector
from mysql.connector import errorcode
from discord import Embed, Colour, Guild, TextChannel
from discord.ext import commands
from discord.utils import get
import re
import json
import random
import time

# Loading config file...
with open("./config.json", "r", encoding="utf-8") as config:
    configFile = json.load(config)
    config.close()

class ChatControl(commands.Cog, name="Chat management commands"):
    def __init__(self, client):
        self.client = client

        print(f' >> Connecting to database with user {configFile["db-settings"]["user"]}!')

        try:
            self.connection = mysql.connector.connect(
                host=f'{configFile["db-settings"]["address"]}',
                user=f'{configFile["db-settings"]["user"]}',
                password=f'{configFile["db-settings"]["password"]}',
                database=f'{configFile["db-settings"]["database"]}',
                autocommit=True
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
    
    # External functions
    async def list_channels(self, ctx, args):
        guild_id = ctx.message.guild.id

        # UI
        embed = Embed(title="ExpertiseBot Channel Backup Utility",
                      description="Using ExpertiseBot to create a backup of every message from any text channel available in this server (except private channels).")
        embed.color = 0x5CA7AD
        embed.add_field(
            name="How to:", value="To create a backup you must set the channels to be watched and backup every message!", inline=False)

        # Selecting all channels in database
        sql_list_channels = """
            SELECT
                `id`,
                `guild_id`,
                `name`,
                `fl_backup`,
                `fl_log`,
                `fl_active`,
                `fl_deleted`,
                `deleted_at`
            FROM
                sec_channels
            WHERE 
                `guild_id` = %s
            ORDER BY `name` ASC;
        """
        self.cursor.execute(sql_list_channels, (guild_id,))

        found_channels = self.cursor.fetchall()

        # Adding results to Embed
        for channel in found_channels:
            log_channel = False
            backing_up = False

            if channel[3] == 1:
                backing_up = True

            if channel[4] == 1:
                log_channel = True

            embed.add_field(
                name=f"{channel[2]}:",
                value=f"Backup enabled: {'✔️' if backing_up else '❌'}{' | 🖨️' if log_channel else ''}",
                inline=False
            )

        embed.set_footer(text="Log channel: 🖨️")

        # Send embed
        await ctx.send(embed=embed)

        return True

    async def setup_backup(self, ctx, args):
        message = ctx.message
        guild = ctx.guild
        guild_id = guild.id
        guild_text_channels = guild.text_channels

        # Starting SQL stuff
        sql_guilds = """INSERT IGNORE INTO sec_guilds (`id`, `name`) VALUES (%s, %s);"""
        
        # Commiting changes to DB
        self.cursor.execute(sql_guilds, (guild.id, guild.name))
        self.connection.commit()

        server_inserted = self.cursor.rowcount

        if server_inserted < 1:
            await ctx.send("Server already exists in database!")
            
        channels = []

        sql_channels = """
            INSERT IGNORE INTO sec_channels (
                `id`,
                `guild_id`,
                `name`,
                `fl_backup`,
                `fl_log`,
                `fl_active`,
                `fl_deleted`,
                `deleted_at`
            ) VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            );
        """

        for channel in guild_text_channels:
            cnnl = (channel.id, guild_id, channel.name, 0, 0, 1, 0, None)
            channels.append(cnnl)
        
        self.cursor.executemany(sql_channels, channels)
        self.connection.commit()

        channels_inserted = self.cursor.rowcount

        channels.clear()

        if server_inserted > 0:
            success = Embed(
                title="ExpertiseBot Channel Backup Utility",
                description="Success! Server registered successfully!"
            )
            
            success.add_field(
                title="Whats next?",
                description=f"Run `{configFile['config']['default_prefix']}backup list`"
            )

            success.color = 0x0E8A00
            await ctx.send(embed=success)

        return True
    
    async def setup_set_log(self, ctx, channel):
        if len(channel) < 1:
            await ctx.send("Cannot set a Null channel to be the log! :confounded:")
            return False
        
        guild_id = ctx.message.guild.id
        channel_id = re.sub(r'[^\d]+', '', channel[0])

        channel = get(ctx.message.guild.text_channels, id=int(channel_id))

        pre_update_sql = """SELECT COUNT(*), id FROM sec_channels WHERE `guild_id` = %s AND `fl_log` = 1;"""

        self.cursor.execute(pre_update_sql, (guild_id,))

        found_channels = self.cursor.fetchall()

        if found_channels[0][0] > 0:
            await ctx.send(f"Hmmm :confused:, it looks like there is another channel set as log channel! Please run `{configFile['config']['default_prefix']}backup list` to check which channel is!")
            return False

        update_channel_sql = """UPDATE sec_channels SET `fl_log` = 1 WHERE `id` = %s AND `guild_id` = %s;"""
        
        self.cursor.execute(update_channel_sql, (channel_id, guild_id,))
        self.connection.commit()

        updated = self.cursor.rowcount

        if updated == 0:
            await ctx.send(f"Cannot set {channel.mention} as a log channel! :confused:")
            return False

        success = Embed(
            title="ExpertiseBot Channel Backup Utility",
            description=f"Success! {channel.mention} was set as log channel successfully!"
        )

        success.color = 0x0E8A00

        await ctx.send(embed=success)             
    
    async def setup_unset_log(self, ctx, channel):
        if len(channel) < 1:
            await ctx.send("Cannot set a Null channel to be the log! :confounded:")
            return False

        guild_id = ctx.message.guild.id
        channel_id = re.sub(r'[^\d]+', '', channel[0])

        channel = get(ctx.message.guild.text_channels, id=int(channel_id))

        pre_update_sql = """SELECT COUNT(*), id FROM sec_channels WHERE `guild_id` = %s AND `fl_log` = 1;"""

        self.cursor.execute(pre_update_sql, (guild_id,))

        found_channels = self.cursor.fetchall()

        if found_channels[0][0] < 1:
            await ctx.send(f"Hmmm :confused:, it looks like there's no channel set as log channel!")
            return False

        update_channel_sql = """UPDATE sec_channels SET `fl_log` = 0 WHERE `id` = %s AND `guild_id` = %s;"""

        self.cursor.execute(update_channel_sql, (channel_id, guild_id,))
        self.connection.commit()

        updated = self.cursor.rowcount

        if updated == 0:
            await ctx.send(f"Cannot unset {channel.mention} as a log channel! :confused:")
            return False

        success = Embed(
            title="ExpertiseBot Channel Backup Utility",
            description=f"Success! {channel.mention} is no longer a log channel!"
        )

        success.color = 0x0E8A00

        await ctx.send(embed=success)

    # Backup enable and disable functions
    async def backup_enable(self, ctx, channel):
        guild_id = ctx.message.guild.id
        channel_id = re.sub(r'[^\d]+', '', channel[0])

        get_channel_sql = """SELECT `id` FROM sec_channels WHERE id = %s AND guild_id = %s"""
        self.cursor.execute(get_channel_sql, (channel_id, guild_id,))


    # Commands
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
    async def backup(self, ctx, command, *args):
        commands = {
            "list": self.list_channels,
            "setup": self.setup_backup,
            "setlog": self.setup_set_log,
            "unsetlog": self.setup_unset_log,
            "enable": self.backup_enable,
            "disable": '',
            "restore": ''
        }

        return await commands[command](ctx, args)
    
    # Events
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        insert_channel_sql = """
            INSERT IGNORE INTO sec_channels (
                `id`,
                `guild_id`,
                `name`,
                `fl_backup`,
                `fl_log`,
                `fl_active`,
                `fl_deleted`,
                `deleted_at`
            ) VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            );
        """

        self.cursor.execute(insert_channel_sql, (channel.id, channel.guild.id, channel.name, 0, 0, 1, 0, None))
        self.connection.commit()

        channel_inserted = self.cursor.rowcount
        
        if channel_inserted > 0:
            success = Embed(title="ExpertiseBot Channel Backup Utility", description="Success! Channel successfully registered!")
            success.color = 0x0E8A00
            success.add_field(name="To add it to backup list",
                              value=f"run `{configFile['config']['default_prefix']}backup add {channel.mention}`")

            await channel.send(embed=success)
        else:
            error = Embed(title="ExpertiseBot Channel Backup Utility", description="Error! Couldn't register channel!")
            error.color = 0xFF0000
            error.add_field(name="Maybe this server is not registered yet... To do that",
                              value=f"run `{configFile['config']['default_prefix']}backup setup`")

            await channel.send(embed=error)

        return True

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        update_channel_deleted_sql = """UPDATE `sec_channels` SET `fl_deleted` = %s, `deleted_at` = %s WHERE id = %s"""
        
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        
        print(now)

        self.cursor.execute(update_channel_deleted_sql, (1, now, channel.id,))
        self.connection.commit()

        # remove_channel_sql = """
        #     DELETE FROM sec_channels WHERE `id` = %s;
        # """

        # self.cursor.execute(remove_channel_sql, (channel.id,))
        # self.connection.commit()

        print(channel.guild.owner)
        

def setup(client):
    client.add_cog(ChatControl(client))
