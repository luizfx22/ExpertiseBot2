from libs import utils
from colorama import init as colinit
from colorama import Fore, Back, Style
import json
import math
import os
import datetime

# Discord
import discord
from discord.ext import commands, tasks

# Loading config file...
with open("./config.json", "r", encoding="utf-8") as config:
    configFile = json.load(config)

# Initializing colorama
colinit()

# Defining the token (got from config.json file)
token = configFile["config"]["token"]

# Defining the bot command prefix
prefix = configFile["config"]["default_prefix"]

# Initializing the client
client = commands.Bot(command_prefix=prefix, self_bot=False)

activity = discord.Activity(name=f"Use {prefix}help para ajuda!", type=discord.ActivityType.watching)


# Doing some work at startup...
@client.event
async def on_ready():
    utils.Eb2Utils.clear()
    
    # Formatting the clients name to fit into the box        
    name = str(client.user)
    name_length = len(name)
    act_char = 0
    name_ = ""
    if name_length > 18:
        name.split(name[18])
        for char in name:
            name_ += char
            if act_char == 18:
                name_ += "..."
                break            
            act_char += 1
    else:
        name_ = name

    await client.change_presence(status=discord.Status.online, activity=activity)

    print(f"\n {Fore.LIGHTBLUE_EX}ExpertiseBot² Core{Style.RESET_ALL}\n")
    RefreshConsoleStatus.start()
    
@tasks.loop(seconds=5)
async def RefreshConsoleStatus():
    clientLatency = math.floor(client.latency * 1000)
    clientGuilds = len(list(client.guilds))
    
    os.system(f"TITLE ExpertiseBot2 Core v0.0.2 :: Ping: {clientLatency}ms :: # Guilds: {clientGuilds}")

if __name__ == '__main__':
    print(" Preparing to start...")
    print(" Loading cogs...")
    try:
        client.load_extension('extensions.ext_mgr')
    except Exception as err:
        print(f" ~ An error occurred whilst loading all cogs!\n{err}")
        exit

# Running the client
client.run(configFile["config"]["token"])
