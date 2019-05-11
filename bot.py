import discord
import asyncio
import json



# Loading config file...
with open("./config.json", "r", encoding="utf-8") as config:
    j = json.load(config)

# Defining the token (got from .json file)
token = j["config"]["token"]

# Initializing the client
client = discord.Client()

# Doing some work at startup...
@client.event
async def on_ready():
    print (" => Bot online!")


# Running the client
client.run(token)
