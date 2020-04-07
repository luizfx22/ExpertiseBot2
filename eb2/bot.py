from libs import utils
import json

# Discord
import discord
from discord.ext import commands

# Loading config file...
with open("./config.json", "r", encoding="utf-8") as config:
    configFile = json.load(config)

# Defining the token (got from config.json file)
token = configFile["config"]["token"]

# Defining the bot command prefix
prefix = configFile["config"]["default_prefix"]

# Initializing the client
client = commands.Bot(command_prefix=prefix, self_bot=False)
activity = discord.Game(name=f"Use {prefix}help for help!")


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
    
    # The box    
    print(" ╔══════════════════════════════════════╗")
    print(" ║       Welcome to ExpertiseBot!       ║")
    print(" ╟──────────────────────────────────────╢")
    print(" ║{: ^38}║".format(name_))
    print(" ╚══════════════════════════════════════╝")
    
    await client.change_presence(status=discord.Status.online, activity=activity)
    print("\n Logs:\n")

if __name__ == '__main__':
    try:
        client.load_extension('extensions.ext_mgr')
    except Exception as err:
        print(f" ~ An error occurred whilst loading all cogs!\n{err}")
        exit

# Running the client
client.run(["config"]["token"])
