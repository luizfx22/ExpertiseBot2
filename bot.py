import discord
import json

with open("./config.json", "r", encoding="utf-8") as config:
    j = config.dump()
    config.Close()
    
print (j["config"]["token"])

client = discord.Client()



