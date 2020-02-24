from os import system, name
import json

# Discord
import discord
from discord.ext import commands


# Simple function to clear the console...
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
        _ = system('TITLE Expertise Bot :: Rewrite v0.0.1')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
        

# Loading config file...
with open("./config.json", "r", encoding="utf-8") as config:
    j = json.load(config)

# Defining the token (got from .json file)
token = j["config"]["token"]

# Defining prefix from config
prefix = j["config"]["prefix"]

# Initializing the client
client = commands.Bot(command_prefix=prefix)
activity = discord.Game(name=f"Use {prefix}help for help!")


# Doing some work at startup...
@client.event
async def on_ready():
    clear()
    
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
    print(" ║ => We're ready to go!                ║")
    print(" ╟──────────────────────────────────────╢")
    print(" ║{: ^38}║".format(name_))
    print(" ╟──────────────────────────────────────╢")
    print(" ╚══════════════════════════════════════╝")
    
    # Console screen title (just for, idk, make it better, i guess)
    system('TITLE Expertise Bot Core :: Rewrite v0.0.1 :: Online as [ {} ]'.format(name))
    await client.change_presence(status=discord.Status.online, activity=activity)

if __name__ == '__main__':
    client.load_extension('extensions.cog_man')




# Running the client
client.run(token)
